from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
import csv

from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT

from gui.toolbar import Toolbar
from gui.sensor_panel import SensorPanel
from gui.plot_panel import PlotPanel
from gui.status_panel import StatusPanel

from hardware.acquisition_thread import AcquisitionThread

from models.data_recorder import DataRecorder
from models.run_history import RunHistory


class MainWindow(QMainWindow):

    def __init__(self, manager=None):
        super().__init__()

        self.manager = manager
        self.thread = None

        self.recorder = DataRecorder()
        self.run_history = RunHistory()

        # Always have at least one run available
        self.run_history.start_new_run()

        self.setWindowTitle(APP_NAME)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # -----------------------
        # Central Widget
        # -----------------------

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # -----------------------
        # Widgets
        # -----------------------

        self.toolbar = Toolbar()
        self.sensor_panel = SensorPanel()
        self.plot_panel = PlotPanel()
        self.status_panel = StatusPanel()

        # -----------------------
        # Connections
        # -----------------------

        self.toolbar.run_button.clicked.connect(self.toggle_acquisition)
        self.toolbar.save_button.clicked.connect(self.save_csv)
        self.toolbar.clear_button.clicked.connect(self.clear_everything)
        self.sensor_panel.button_group.buttonClicked.connect(self.sensor_changed)

        # -----------------------
        # Layout
        # -----------------------

        center_layout = QHBoxLayout()

        center_layout.addWidget(self.sensor_panel, 1)
        center_layout.addWidget(self.plot_panel, 4)

        main_layout.addWidget(self.toolbar)
        main_layout.addLayout(center_layout)
        main_layout.addWidget(self.status_panel)

        # -----------------------
        # Initial View
        # -----------------------

        self.current_sensor = self.sensor_panel.selected_sensor()

        if self.current_sensor == -1:
            self.plot_panel.show_all()
        else:
            self.plot_panel.show_single()

    # ==========================================================
    # Acquisition
    # ==========================================================

    def start_acquisition(self):

        if self.thread is not None and self.thread.isRunning():
            return

        try:
            self.manager.connect()
            self.sensor_panel.set_available_sensor_ids(
                self.manager.sensor_ids
            )

        except Exception as e:

            self.toolbar.status_label.setText(f"Error: {e}")

            return

        # Start a NEW run unless continuing
        if not self.toolbar.continue_checkbox.isChecked():

            self.plot_panel.clear()

            self.recorder.clear()

            self.run_history.start_new_run()

        self.thread = AcquisitionThread(self.manager)

        self.thread.data_ready.connect(self.update_display)
        self.thread.error.connect(self.acquisition_error)

        self.thread.start()

        self.toolbar.set_running()

        # Disable controls while acquiring
        self.toolbar.continue_checkbox.setEnabled(False)
        self.toolbar.save_button.setEnabled(False)
        self.toolbar.clear_button.setEnabled(False)

    def stop_acquisition(self):

        if self.thread is None:
            return

        self.thread.stop()

        self.thread.wait()

        self.thread = None

        try:
            self.manager.disconnect()
        except Exception:
            pass

        self.toolbar.set_idle()

        # Re-enable controls
        self.toolbar.continue_checkbox.setEnabled(True)
        self.toolbar.save_button.setEnabled(True)
        self.toolbar.clear_button.setEnabled(True)

    # ==========================================================
    # Display
    # ==========================================================

    def update_display(self, readings):

        if not readings:
            self.toolbar.status_label.setText("Status: No sensors responding")
            return

        # -----------------------
        # Record Data
        # -----------------------

        self.recorder.add_sample(readings)

        self.run_history.add_sample(
            self.recorder.get_data()[-1]
        )

        self.plot_panel.append_readings(readings)

        # -----------------------
        # Detect sensor change
        # -----------------------

        selected = self.sensor_panel.selected_sensor()

        if selected != self.current_sensor:

            self.current_sensor = selected

            if selected == -1:

                self.plot_panel.show_all()

                self.plot_panel.update_all()

            else:

                self.plot_panel.show_single()

                self.plot_panel.update_sensor(
                    self.current_sensor
                )

        # -----------------------
        # View All
        # -----------------------

        if self.current_sensor == -1:

            self.plot_panel.update_all()

            # Show the first connected sensor in the status panel. The
            # notebook intentionally skips empty mux channels.
            first = readings[0]

            self.status_panel.bx.setText(
                f"Bx: {first.bx:.2f} μT"
            )

            self.status_panel.by.setText(
                f"By: {first.by:.2f} μT"
            )

            self.status_panel.bz.setText(
                f"Bz: {first.bz:.2f} μT"
            )

            self.status_panel.mag.setText(
                f"|B|: {first.magnitude:.2f} μT"
            )

            return

        # -----------------------
        # Single Sensor
        # -----------------------

        reading = next(
            (item for item in readings if item.sensor_id == self.current_sensor),
            None,
        )
        if reading is None:
            return


        self.plot_panel.update_sensor(self.current_sensor)

        self.status_panel.bx.setText(
            f"Bx: {reading.bx:.2f} μT"
        )

        self.status_panel.by.setText(
            f"By: {reading.by:.2f} μT"
        )

        self.status_panel.bz.setText(
            f"Bz: {reading.bz:.2f} μT"
        )

        self.status_panel.mag.setText(
            f"|B|: {reading.magnitude:.2f} μT"
        )

    def acquisition_error(self, message):
        self.toolbar.status_label.setText(f"Status: Acquisition error: {message}")
        self.stop_acquisition()

    # ==========================================================
    # Clear
    # ==========================================================

    def clear_everything(self):

        # Stop acquisition first
        self.stop_acquisition()

        self.plot_panel.clear()

        self.recorder.clear()

        self.run_history.clear()

        self.run_history.start_new_run()

        self.toolbar.set_idle()

    # ==========================================================
    # Close
    # ==========================================================

    def closeEvent(self, event):

        self.stop_acquisition()

        event.accept()
    
    def sensor_changed(self):

        self.current_sensor = (
            self.sensor_panel.selected_sensor()
        )

        if self.current_sensor == -1:

            self.plot_panel.show_all()

            self.plot_panel.update_all()

        else:

            self.plot_panel.show_single()

            self.plot_panel.update_sensor(
                self.current_sensor
            )

    def toggle_acquisition(self):

        if self.thread is None:

            self.start_acquisition()

        elif self.thread.isRunning():

            self.stop_acquisition()

        else:

            self.start_acquisition()

    def save_csv(self):
        rows = self.recorder.get_data()
        if not rows:
            self.toolbar.status_label.setText("Status: No data to save")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save magnetic field data",
            "helmholtz_measurements.csv",
            "CSV files (*.csv)",
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as output:
                writer = csv.writer(output)
                writer.writerow(DataRecorder.headers())
                writer.writerows(rows)
        except OSError as error:
            QMessageBox.critical(self, "Save failed", str(error))
            return

        self.toolbar.status_label.setText(f"Status: Saved {path}")
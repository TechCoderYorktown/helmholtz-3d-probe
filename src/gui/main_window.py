from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

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

        self.recorder = DataRecorder()
        self.run_history = RunHistory()
        self.manager = manager
        self.thread = None

        self.setWindowTitle(APP_NAME)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        self.toolbar = Toolbar()
        self.toolbar.run_button.clicked.connect(self.start_acquisition)
        self.toolbar.stop_button.clicked.connect(self.stop_acquisition)
        self.sensor_panel = SensorPanel()
        self.plot_panel = PlotPanel()
        self.toolbar.clear_button.clicked.connect(self.plot_panel.clear)
        self.toolbar.clear_button.clicked.connect(self.clear_everything)
        self.status_panel = StatusPanel()

        center_layout = QHBoxLayout()
        center_layout.addWidget(self.sensor_panel, 1)
        center_layout.addWidget(self.plot_panel, 4)

        main_layout.addWidget(self.toolbar)
        main_layout.addLayout(center_layout)
        main_layout.addWidget(self.status_panel)

        self.current_sensor = self.sensor_panel.selected_sensor()

        if self.current_sensor == -1:
            self.plot_panel.show_all()
        else:
            self.plot_panel.show_single()

    def start_acquisition(self):

        if self.thread is not None and self.thread.isRunning():
            return

        try:
            self.manager.connect()
        except Exception as e:
            self.toolbar.status_label.setText(f"Error: {e}")
            return

        if not self.toolbar.continue_checkbox.isChecked():
            self.plot_panel.clear()
            self.recorder.clear()
            self.run_history.start_new_run()

        self.thread = AcquisitionThread(self.manager)

        self.thread.data_ready.connect(self.update_display)

        self.thread.start()

        self.toolbar.status_label.setText("Status: Running")

    def stop_acquisition(self):

        if self.thread is None:
            return

        self.thread.stop()
        self.thread.wait()

        self.thread = None

        self.manager.disconnect()

        self.toolbar.status_label.setText("Status: Stopped")

    def update_display(self, readings):

        if not readings:
            return

        self.recorder.add_sample(readings)
        self.run_history.add_sample(self.recorder.get_data()[-1])

        selected = self.sensor_panel.selected_sensor()

        if selected != self.current_sensor:
            self.current_sensor = selected

            if selected == -1:
                self.plot_panel.show_all()
            else:
                self.plot_panel.show_single()

        if self.current_sensor == -1:
            self.plot_panel.update_all(readings)
            return

        if self.current_sensor >= len(readings):
            return

        reading = readings[self.current_sensor]

        self.plot_panel.update_sensor(reading)

        self.status_panel.bx.setText(f"Bx: {reading.bx:.2f} μT")
        self.status_panel.by.setText(f"By: {reading.by:.2f} μT")
        self.status_panel.bz.setText(f"Bz: {reading.bz:.2f} μT")
        self.status_panel.mag.setText(f"|B|: {reading.magnitude:.2f} μT")

    def closeEvent(self, event):

        self.stop_acquisition()

        event.accept()

    def clear_everything(self):

        self.plot_panel.clear()

        self.recorder.clear()

        self.run_history.clear()

        self.run_history.start_new_run()

        self.toolbar.status_label.setText("Status: Idle")
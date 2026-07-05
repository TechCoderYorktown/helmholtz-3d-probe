import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QGridLayout


class PlotPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.stack = QStackedLayout()
        layout.addLayout(self.stack)

        # ----- Single Sensor Plot -----
        single_widget = QWidget()
        single_layout = QVBoxLayout(single_widget)

        self.plot = pg.PlotWidget()
        self.plot.addLegend()
        self.plot.enableAutoRange()
        self.plot.setTitle("Live Magnetic Field", size="14pt")
        self.plot.setLabel("left", "Magnetic Field", units="μT")
        self.plot.setLabel("bottom", "Samples")
        self.plot.showGrid(x=True, y=True, alpha=0.3)

        self.curve_x = self.plot.plot(name="Bx", pen=pg.mkPen((255, 80, 80), width=2))
        self.curve_y = self.plot.plot(name="By", pen=pg.mkPen((80, 255, 80), width=2))
        self.curve_z = self.plot.plot(name="Bz", pen=pg.mkPen((80, 150, 255), width=2))

        single_layout.addWidget(self.plot)
        self.stack.addWidget(single_widget)

        # ----------------------------
        # Single-view data storage
        # One history per sensor
        # ----------------------------

        self.sensor_data = []

        for _ in range(8):

            self.sensor_data.append(
                {
                    "x": [],
                    "y": [],
                    "z": [],
                }
            )

        # ----- All Sensors Widget -----
        all_widget = QWidget()
        grid = QGridLayout(all_widget)

        self.all_plots = []

        for i in range(8):
            plot = pg.PlotWidget()
            plot.setTitle(f"Sensor {i}")
            plot.showGrid(x=True, y=True)
            plot.addLegend()

            x_curve = plot.plot(name="Bx", pen="r")
            y_curve = plot.plot(name="By", pen="g")
            z_curve = plot.plot(name="Bz", pen="b")

            self.all_plots.append(
            {
                "plot": plot,
                "x": x_curve,
                "y": y_curve,
                "z": z_curve,
            }
            )

            grid.addWidget(plot, i // 2, i % 2)

        self.stack.addWidget(all_widget)

        self.max_points = 500
        self.set_single_view()

    def set_single_view(self):
        self.stack.setCurrentIndex(0)

    def set_all_view(self):
        self.stack.setCurrentIndex(1)

    def update_sensor(self, sensor_index):
        """
        Redraw one sensor using its stored history.
        """

        sensor = self.sensor_data[sensor_index]

        self.curve_x.setData(sensor["x"])

        self.curve_y.setData(sensor["y"])

        self.curve_z.setData(sensor["z"])

    def update_all(self):

        for i in range(8):

            sensor = self.sensor_data[i]

            plot = self.all_plots[i]

            plot["x"].setData(sensor["x"])

            plot["y"].setData(sensor["y"])

            plot["z"].setData(sensor["z"])

    def append_readings(self, readings):
        """
        Store every incoming sample for every sensor.
        """

        for i, reading in enumerate(readings[:8]):

            # -------- Single View History --------

            sensor = self.sensor_data[i]

            sensor["x"].append(reading.bx)
            sensor["y"].append(reading.by)
            sensor["z"].append(reading.bz)

            if len(sensor["x"]) > self.max_points:
                sensor["x"].pop(0)
                sensor["y"].pop(0)
                sensor["z"].pop(0)

    def clear(self):

        for sensor in self.sensor_data:

            sensor["x"].clear()
            sensor["y"].clear()
            sensor["z"].clear()

        self.curve_x.setData([])
        self.curve_y.setData([])
        self.curve_z.setData([])

        for plot in self.all_plots:

            plot["x"].setData([])
            plot["y"].setData([])
            plot["z"].setData([])

    def show_single(self):
        self.stack.setCurrentIndex(0)

    def show_all(self):
        self.stack.setCurrentIndex(1)
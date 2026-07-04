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

        self.x_data = []
        self.y_data = []
        self.z_data = []

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
                    "xdata": [],
                    "ydata": [],
                    "zdata": [],
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

    def update_sensor(self, sensor_reading):

        self.x_data.append(sensor_reading.bx)
        self.y_data.append(sensor_reading.by)
        self.z_data.append(sensor_reading.bz)

        if len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.y_data.pop(0)
            self.z_data.pop(0)

        self.curve_x.setData(self.x_data)
        self.curve_y.setData(self.y_data)
        self.curve_z.setData(self.z_data)

    def update_all(self, readings):

        for i, reading in enumerate(readings[:8]):
            plot_data = self.all_plots[i]

            plot_data["xdata"].append(reading.bx)
            plot_data["ydata"].append(reading.by)
            plot_data["zdata"].append(reading.bz)

            if len(plot_data["xdata"]) > self.max_points:
                plot_data["xdata"].pop(0)
                plot_data["ydata"].pop(0)
                plot_data["zdata"].pop(0)

            plot_data["x"].setData(plot_data["xdata"])
            plot_data["y"].setData(plot_data["ydata"])
            plot_data["z"].setData(plot_data["zdata"])

    def clear(self):

        self.x_data.clear()
        self.y_data.clear()
        self.z_data.clear()

        self.curve_x.setData([])
        self.curve_y.setData([])
        self.curve_z.setData([])

        for plot_data in self.all_plots:
            plot_data["xdata"].clear()
            plot_data["ydata"].clear()
            plot_data["zdata"].clear()

            plot_data["x"].setData([])
            plot_data["y"].setData([])
            plot_data["z"].setData([])

    def show_single(self):
        self.stack.setCurrentIndex(0)

    def show_all(self):
        self.stack.setCurrentIndex(1)
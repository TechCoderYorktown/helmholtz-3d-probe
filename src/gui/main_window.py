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


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        self.toolbar = Toolbar()
        self.sensor_panel = SensorPanel()
        self.plot_panel = PlotPanel()
        self.status_panel = StatusPanel()

        center_layout = QHBoxLayout()
        center_layout.addWidget(self.sensor_panel, 1)
        center_layout.addWidget(self.plot_panel, 4)

        main_layout.addWidget(self.toolbar)
        main_layout.addLayout(center_layout)
        main_layout.addWidget(self.status_panel)
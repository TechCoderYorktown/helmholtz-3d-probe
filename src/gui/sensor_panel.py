from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QRadioButton


class SensorPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Sensors"))

        layout.addWidget(QRadioButton("All"))

        for i in range(8):
            layout.addWidget(QRadioButton(f"Sensor {i}"))

        layout.addStretch()

        self.setLayout(layout)
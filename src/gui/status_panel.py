from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QHBoxLayout


class StatusPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.bx = QLabel("Bx: -- μT")
        self.by = QLabel("By: -- μT")
        self.bz = QLabel("Bz: -- μT")
        self.mag = QLabel("|B|: -- μT")

        layout.addWidget(self.bx)
        layout.addWidget(self.by)
        layout.addWidget(self.bz)

        layout.addStretch()

        layout.addWidget(self.mag)

        self.setLayout(layout)
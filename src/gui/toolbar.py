from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QHBoxLayout


class Toolbar(QWidget):

    def __init__(self):
        super().__init__()

        self.run_button = QPushButton("▶ Run")
        self.stop_button = QPushButton("■ Stop")
        self.save_button = QPushButton("💾 Save CSV")
        self.clear_button = QPushButton("🗑 Clear")

        self.status_label = QLabel("Status: Idle")

        layout = QHBoxLayout()

        layout.addWidget(self.run_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.clear_button)

        layout.addStretch()

        layout.addWidget(self.status_label)

        self.setLayout(layout)
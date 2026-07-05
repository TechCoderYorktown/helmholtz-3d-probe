import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from hardware.hardware_manager import HardwareManager


def main():
    app = QApplication(sys.argv)

    # Change to False when the FT232H and sensors are connected.
    manager = HardwareManager(simulate=True)

    window = MainWindow(manager)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
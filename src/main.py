import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from hardware.simulator_manager import SimulatorManager


def main():
    app = QApplication(sys.argv)

    manager = SimulatorManager()

    window = MainWindow(manager)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
import sys
import argparse

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from hardware.hardware_manager import HardwareManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Use the simulator instead of the hardware backend.",
    )
    args, qt_args = parser.parse_known_args()

    app = QApplication(sys.argv)

    if args.simulate:
        print("Starting in SIMULATION mode.")
    else:
        print("Starting in HARDWARE mode.")

    manager = HardwareManager(simulate=args.simulate)

    window = MainWindow(manager)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal

import time


class AcquisitionThread(QThread):

    data_ready = Signal(list)

    def __init__(self, manager):

        super().__init__()

        self.manager = manager

        self.running = False

    def run(self):
        self.running = True

        while self.running:
            readings = self.manager.read_all()
            self.data_ready.emit(readings)

            self.msleep(100)   # 10 Hz update rate

    def stop(self):
        
        self.running = False
from PySide6.QtCore import QThread, Signal

import time


class AcquisitionThread(QThread):

    data_ready = Signal(list)
    error = Signal(str)

    def __init__(self, manager):

        super().__init__()

        self.manager = manager

        self.running = False

    def run(self):
        self.running = True

        while self.running:
            try:
                readings = self.manager.read_all()
            except Exception as error:
                self.error.emit(str(error))
                break
            self.data_ready.emit(readings)

            self.msleep(100)   # 10 Hz update rate
        self.running = False

    def stop(self):
        
        self.running = False
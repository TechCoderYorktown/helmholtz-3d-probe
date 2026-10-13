from hardware.simulator_manager import SimulatorManager


class HardwareManager:

    def __init__(self, simulate=True):

        self.simulate = simulate

        if simulate:
            self.manager = SimulatorManager()
        else:
            from hardware.mmc5603_manager import MMC5603Manager

            self.manager = MMC5603Manager()

    @property
    def sensor_ids(self):
        if self.simulate:
            return list(range(8))
        return self.manager.sensor_ids

    def connect(self):
        self.manager.connect()

    def disconnect(self):
        self.manager.disconnect()

    def read_all(self):
        return self.manager.read_all()
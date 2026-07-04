import math
import time

from models.sensor_reading import SensorReading


class SimulatorManager:

    def connect(self):
        print("Simulator connected.")

    def disconnect(self):
        print("Simulator disconnected.")

    def read_all(self):

        t = time.time()

        readings = []

        for sensor in range(8):

            phase = sensor * 0.3

            bx = 30 * math.sin(t + phase)
            by = 20 * math.cos(t * 0.8 + phase)
            bz = 45 + 5 * math.sin(t * 0.5 + phase)

            readings.append(
                SensorReading.now(
                    sensor,
                    bx,
                    by,
                    bz
                )
            )

        return readings
from hardware.ft232h import FT232HConnection

import adafruit_tca9548a
import adafruit_mmc56x3

from models.sensor_reading import SensorReading


class SensorManager:

    def __init__(self):

        self.connected = False

        self.connection = FT232HConnection()

        self.i2c = None

        self.mux = None

        self.sensors = []

    def connect(self):

        if self.connected:
            return

        self.i2c = self.connection.connect()

        self.mux = adafruit_tca9548a.TCA9548A(self.i2c)

        self.sensors = [

            adafruit_mmc56x3.MMC5603(
                self.mux[channel]
            )

            for channel in range(8)

        ]


        self.connected = True
        print("Connected to 8 sensors.")

    def read_all(self):

        readings = []

        for sensor_id, sensor in enumerate(self.sensors):

            try:

                bx, by, bz = sensor.magnetic

            except Exception:

                print(f"Sensor {sensor_id} failed: {e}")

                bx = float("nan")
                by = float("nan")
                bz = float("nan")

            readings.append(

                SensorReading.now(
                    sensor_id,
                    bx,
                    by,
                    bz
                )

            )

        return readings

    def disconnect(self):

        self.sensors.clear()

        self.mux = None

        self.i2c = None

        self.connected = False
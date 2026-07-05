import os
import usb.backend.libusb1
import libusb_package

import board

import adafruit_tca9548a
import adafruit_mmc56x3

from hardware.sensor_reading import SensorReading

class MMC5603Manager:

    def __init__(self):

        self.connected = False

        self.sensors = []

    def connect(self):

        if self.connected:
            return

        try:

            os.environ["BLINKA_FT232H"] = "1"

            _original_get_backend = usb.backend.libusb1.get_backend

            def _patched_get_backend(find_library=None, *args, **kwargs):
                return _original_get_backend(
                    find_library=libusb_package.find_library,
                    *args,
                    **kwargs
                )

            usb.backend.libusb1.get_backend = _patched_get_backend

            self.i2c = board.I2C()

            self.mux = adafruit_tca9548a.TCA9548A(self.i2c)

            # Verify channels (optional but useful)
            for ch in range(8):

                channel = self.mux[ch]

                while not channel.try_lock():
                    pass

                try:
                    addresses = [hex(a) for a in channel.scan()]
                    print(f"Channel {ch}: {addresses}")

                finally:
                    channel.unlock()

            self.sensors = [
                adafruit_mmc56x3.MMC5603(self.mux[ch])
                for ch in range(8)
            ]

            self.connected = True

            print(f"Initialized {len(self.sensors)} sensors.")

        except Exception:

            self.connected = False

            raise

    def read_all(self):

        if not self.connected:
            raise RuntimeError("Hardware is not connected.")

        readings = []

        for i, sensor in enumerate(self.sensors):

            try:

                x, y, z = sensor.magnetic

            except Exception as e:

                print(f"Sensor {i} read failed: {e}")

                x = float("nan")
                y = float("nan")
                z = float("nan")

            readings.append(

                SensorReading(

                    sensor=i,

                    bx=x,

                    by=y,

                    bz=z,

                )

            )

        return readings
    
    def disconnect(self):

        self.sensors.clear()

        self.mux = None

        self.i2c = None

        self.connected = False
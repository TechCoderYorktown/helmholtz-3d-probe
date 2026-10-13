import os
os.environ["BLINKA_FT232H"] = "1"

import usb.backend.libusb1
import libusb_package
from pyftdi.usbtools import UsbTools

_original_get_backend = usb.backend.libusb1.get_backend

def _patched_get_backend(find_library=None, *args, **kwargs):
    return _original_get_backend(
        find_library=libusb_package.find_library,
        *args,
        **kwargs
    )

usb.backend.libusb1.get_backend = _patched_get_backend


_original_get_string = UsbTools.get_string


def _safe_get_string(cls, device, string_index):
    try:
        return _original_get_string(device, string_index)
    except ValueError as error:
        if "langid" not in str(error).lower():
            raise
        # Some FT232H/libusb driver combinations expose no USB string
        # descriptors. Serial strings are optional for board detection.
        return ""


UsbTools.get_string = classmethod(_safe_get_string)

import board  # must come AFTER the patch above

import adafruit_tca9548a
import adafruit_mmc56x3

from config import (
    I2C_MULTIPLEXER_ADDRESS,
    SENSOR_ADDRESS,
    SENSOR_AXIS_CONFIGS,
)
from models.sensor_reading import SensorReading


class MMC5603Manager:

    def __init__(self):
        self.connected = False
        self.sensors = []
        self.sensor_ids = []

    def connect(self):
        if self.connected:
            return

        try:
            self.i2c = board.I2C()
            self.mux = adafruit_tca9548a.TCA9548A(
                self.i2c,
                address=I2C_MULTIPLEXER_ADDRESS,
            )

            self.sensors = []
            self.sensor_ids = []
            for channel_id in range(8):
                channel = self.mux[channel_id]
                while not channel.try_lock():
                    pass
                try:
                    addresses = channel.scan()
                finally:
                    channel.unlock()

                print(
                    f"Channel {channel_id}: "
                    f"{[hex(address) for address in addresses]}"
                )
                if SENSOR_ADDRESS in addresses:
                    self.sensor_ids.append(channel_id)
                    self.sensors.append(
                        adafruit_mmc56x3.MMC5603(channel)
                    )

            if not self.sensors:
                raise RuntimeError(
                    f"No MMC5603 sensors found at {hex(SENSOR_ADDRESS)}."
                )

            self.connected = True
            print(
                f"Initialized {len(self.sensors)} sensors on channels "
                f"{self.sensor_ids}."
            )

        except Exception:
            self.sensors.clear()
            self.sensor_ids.clear()
            self.connected = False
            raise

    def read_all(self):
        if not self.connected:
            raise RuntimeError("Hardware is not connected.")

        readings = []
        for channel_id, sensor in zip(self.sensor_ids, self.sensors):
            try:
                raw_x, raw_y, raw_z = sensor.magnetic
                transform = SENSOR_AXIS_CONFIGS.get(channel_id)
                if transform is None:
                    x, y, z = raw_x, raw_y, raw_z
                else:
                    x, y, z = transform(raw_x, raw_y, raw_z)
            except Exception as e:
                print(f"Sensor channel {channel_id} read failed: {e}")
                x = float("nan")
                y = float("nan")
                z = float("nan")

            readings.append(SensorReading.now(channel_id, x, y, z))

        return readings

    def disconnect(self):
        self.sensors.clear()
        self.sensor_ids.clear()
        self.mux = None
        self.i2c = None
        self.connected = False
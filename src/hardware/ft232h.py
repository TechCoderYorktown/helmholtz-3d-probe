import os
import usb.backend.libusb1
import libusb_package

import board


class FT232HConnection:

    def __init__(self):

        self.i2c = None

    def connect(self):

        os.environ["BLINKA_FT232H"] = "1"

        original_backend = usb.backend.libusb1.get_backend

        def patched_backend(find_library=None, *args, **kwargs):
            return original_backend(
                find_library=libusb_package.find_library,
                *args,
                **kwargs
            )

        usb.backend.libusb1.get_backend = patched_backend

        self.i2c = board.I2C()

        return self.i2c
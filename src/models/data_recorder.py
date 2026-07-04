import time


class DataRecorder:
    def __init__(self):
        self.clear()

    def clear(self):
        self.start_time = time.perf_counter()
        self.sample = 0
        self.rows = []

    def add_sample(self, readings):
        """
        readings: list[SensorReading]
        """

        elapsed = time.perf_counter() - self.start_time

        row = [
            self.sample,
            elapsed,
        ]

        # Expect up to 8 sensors
        for sensor in readings:
            row.extend([
                sensor.bx,
                sensor.by,
                sensor.bz,
            ])

        self.rows.append(row)
        self.sample += 1

    def get_data(self):
        return self.rows

    @staticmethod
    def headers():
        headers = ["Sample", "Time (s)"]

        for i in range(8):
            headers.extend([
                f"B{i}_X",
                f"B{i}_Y",
                f"B{i}_Z",
            ])

        return headers
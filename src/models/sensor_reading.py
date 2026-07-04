from dataclasses import dataclass
import time
import math


@dataclass
class SensorReading:
    sensor_id: int
    timestamp: float
    bx: float
    by: float
    bz: float

    @property
    def magnitude(self):
        return math.sqrt(
            self.bx**2 +
            self.by**2 +
            self.bz**2
        )

    @classmethod
    def now(cls, sensor_id, bx, by, bz):
        return cls(
            sensor_id=sensor_id,
            timestamp=time.time(),
            bx=bx,
            by=by,
            bz=bz
        )
from collections import deque


class CircularBuffer:

    def __init__(self, max_points=500):
        self.max_points = max_points
        self.buffer = deque(maxlen=max_points)

    def append(self, reading):
        self.buffer.append(reading)

    def clear(self):
        self.buffer.clear()

    def get_all(self):
        return list(self.buffer)

    def __len__(self):
        return len(self.buffer)
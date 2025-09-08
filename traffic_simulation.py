# traffic_simulation.py
import random
import time

class TrafficSimulation:
    def __init__(self, lanes=4, min_cars=0, max_cars=40, refresh_secs=7):
        self.lanes = lanes
        self.min_cars = min_cars
        self.max_cars = max_cars
        self.refresh_secs = refresh_secs
        self._vehicles = [0] * lanes
        self._last_update = 0.0

    def get_vehicle_counts(self):
        now = time.time()
        if now - self._last_update >= self.refresh_secs:
            self._vehicles = [random.randint(self.min_cars, self.max_cars) for _ in range(self.lanes)]
            self._last_update = now
        return list(self._vehicles)

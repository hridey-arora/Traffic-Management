# signal_logic.py
import time
from datetime import datetime

class SignalLogic:
    def __init__(
        self,
        cycle_time=30,          # seconds green for selected lane
        fairness_time=90,       # max time any lane can wait before forced green
        pedestrian_wait=30,     # seconds after request before stopping cars
        pedestrian_cross=15,    # duration of all-red for pedestrians
        pedestrian_cooldown=120 # min seconds between accepted requests
    ):
        self.cycle_time = cycle_time
        self.fairness_time = fairness_time
        self.last_green = [time.time()] * 4
        self.current_green = 0

        # Pedestrian system
        self.ped_requested = False
        self.ped_request_time = None
        self.ped_wait = pedestrian_wait
        self.ped_cross = pedestrian_cross
        self.ped_cooldown = pedestrian_cooldown
        self.ped_last_done = 0.0  # last time a crossing finished

    # ---- Smart scheduling: hour-based lane weights (simple, tweakable) ----
    # Example assumption:
    #   Lane 0,1 = inbound → heavier morning (8-11)
    #   Lane 2,3 = outbound → heavier evening (17-20)
    def _lane_weights(self, hour: int):
        if 8 <= hour <= 11:
            return [1.4, 1.3, 1.0, 1.0]
        if 17 <= hour <= 20:
            return [1.0, 1.0, 1.4, 1.3]
        return [1.0, 1.0, 1.0, 1.0]

    # Public API
    def request_pedestrian(self) -> bool:
        now = time.time()
        # cooldown: ignore spam
        if (now - self.ped_last_done) < self.ped_cooldown or self.ped_requested:
            return False
        self.ped_requested = True
        self.ped_request_time = now
        return True

    def _pedestrian_phase_active(self, now: float) -> bool:
        if not self.ped_requested or self.ped_request_time is None:
            return False
        elapsed = now - self.ped_request_time
        # after waiting window, we stop cars for crossing duration
        return self.ped_wait <= elapsed < (self.ped_wait + self.ped_cross)

    def _pedestrian_maybe_reset(self, now: float):
        if not self.ped_requested or self.ped_request_time is None:
            return
        elapsed = now - self.ped_request_time
        if elapsed >= (self.ped_wait + self.ped_cross):
            # crossing finished
            self.ped_requested = False
            self.ped_request_time = None
            self.ped_last_done = now

    def decide_signals(self, vehicles, emergency_lane=None):
        """
        Returns a list of 4 numbers (seconds of green each lane).
        By design: only one lane gets >0; others remain 0 (red).
        """
        now = time.time()
        signals = [0, 0, 0, 0]

        # 1) Pedestrian crossing (all red during crossing window)
        if self._pedestrian_phase_active(now):
            # keep all red
            return signals
        # If pedestrian cycle is completed, reset flags
        self._pedestrian_maybe_reset(now)

        # 2) Emergency override
        if emergency_lane is not None:
            signals[emergency_lane] = self.cycle_time
            self.last_green[emergency_lane] = now
            self.current_green = emergency_lane
            return signals

        # 3) Fairness: if any lane waited too long, force it green
        for lane in range(4):
            if now - self.last_green[lane] > self.fairness_time:
                signals[lane] = self.cycle_time
                self.last_green[lane] = now
                self.current_green = lane
                return signals

        # 4) Smart scheduling: weight vehicles by time-of-day
        hour = datetime.now().hour
        weights = self._lane_weights(hour)
        weighted = [v * w for v, w in zip(vehicles, weights)]

        # 5) Pick lane with highest weighted demand
        max_lane = max(range(4), key=lambda i: weighted[i])
        signals[max_lane] = self.cycle_time
        self.last_green[max_lane] = now
        self.current_green = max_lane
        return signals

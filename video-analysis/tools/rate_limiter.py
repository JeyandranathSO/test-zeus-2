import time
import threading

class RateLimiter:
    def __init__(self, rpm: int):
        self.min_interval = 60.0 / rpm
        self._lock = threading.Lock()
        self._last_call = 0.0

    def wait(self):
        with self._lock:
            now = time.time()
            elapsed = now - self._last_call

            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)

            self._last_call = time.time()

import time
import math
from typing import Callable

class Alert:
    def __init__(self, on_alert: Callable[[], None], debounce_time = math.inf):
        self.last_alert_time = None
        self.on_alert = on_alert
        self.debounce_time = debounce_time
    
    def alert(self):
        now = time.time()
        if self.last_alert_time is None or now - self.last_alert_time > self.debounce_time:
            self.last_alert_time = now
            self.on_alert()
    
    def reset(self):
        self.last_alert_time = None
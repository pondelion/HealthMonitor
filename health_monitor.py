import threading
from datetime import datetime, timedelta
from time import sleep

from .notifier import (
    Notifier,
    DefaultNotifier
)


class HealthMonitor:

    def __init__(
        self,
        monitoring_target: str,
        max_interval_sec: int = 30*60,
        max_notification_count: int = 5,
        notifier: Notifier = DefaultNotifier(),
    ):
        self._max_interval_sec = max_interval_sec
        self._max_notification_count = max_notification_count
        self._reached_max_notification = False
        self._notifier = notifier
        self._monitoring_target = monitoring_target
        self._monitoring = False
        self._notified_count = 0

    def update(self) -> None:
        self._elapsed_secs_since_last_update = 0
        self._last_updated_datetime = datetime.now()
        self._notified_count = 0

    def start_monitoring(self) -> None:
        self._thread = threading.Thread(self._monitoring_worker)
        self._thread.start()
        self._last_updated_datetime = datetime.now()
        self._monitoring = True
        self._reached_max_notification = False
    
    def stop_monitoring(self) -> None:
        self._monitoring = False

    def _monitoring_worker(self) -> None:
        while self._monitoring:
            dt_now = datetime.now()
            self._elapsed_secs_since_last_update = (dt_now - self._last_updated_datetime).seconds
            if self._elapsed_secs_since_last_update >= self._max_interval_sec:
                self._notify()
                if self._notified_count >= self._max_notification_count:
                    self._reached_max_notification = True
                    self.stop_monitoring()
            sleep(0.2)

    @property
    def reached_max_notification(self) -> bool:
        return self._reached_max_notification

    def _notify(self) -> None:
        self._notified_count += 1
        self._notifier.notify(
            self._monitoring_target,
            self._notified_count
        )

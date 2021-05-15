from threading import Thread
from time import sleep


class MonitorManager:

    def __init__(self):
        self._monitors = {}
        self._thread = Thread(self._monitor_check_worker)
        self._thread.start()

    def register(self, monitor: HealthMonitor, tag: str) -> None:
        if tag in self._monitors:
            raise Exception(f'The HealthMonitor with tag {tag} is already registred.')
        self._monitors[tag] = monitor
        self._monitors[tag].start_monitoring()

    def unregister(self, tag: str) -> None:
        if tag not in self._monitors:
            raise Exception(f'The HealthMonitor with tag {tag} does not exist.')
        del self._monitors[tag]

    def update(self, tag: str):
        if tag not in self._monitors:
            raise Exception(f'The HealthMonitor with tag {tag} does not exist.')
        self._monitors[tag].update()

    def _monitor_check_worker(self):
        while True:
            for tag, monitor in self._monitors:
                if monitor.reached_max_notification:
                    self.unregister(tag)
            sleep(30)

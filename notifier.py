from abc import ABCMeta, abstractmethod

from overrides import overrides


class Notifier(metaclass=ABCMeta):

    @abstractmethod
    def notify(
        self,
        monitoring_target: str,
        notified_cpunt: int
    ) -> None:
        raise NotImplementedError


class MockNotifier(Notifier):

    @overrides
    def notify(
        self,
        monitoring_target: str,
        notified_cpunt: int
    ) -> None:
        print(f'{monitoring_target} : {notified_cpunt}')


DefaultNotifier = MockNotifier


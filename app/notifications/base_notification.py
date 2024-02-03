from abc import ABC, abstractmethod


class BaseNotification(ABC):
    """Абстрактный базовый класс для уведомлений"""

    @abstractmethod
    def send_notification(
        self,
        body: str,
        header: str,
        receivers: list[str],
    ):
        raise NotImplementedError

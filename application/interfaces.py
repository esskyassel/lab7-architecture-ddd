from abc import ABC, abstractmethod
from typing import Protocol

from domain.order import Order
from domain.money import Money


class OrderRepository(Protocol):
    """Интерфейс репозитория заказов."""
    
    def get_by_id(self, order_id: str) -> Order:
        """Получить заказ по ID."""
        ...
    
    def save(self, order: Order) -> None:
        """Сохранить заказ."""
        ...


class PaymentGateway(Protocol):
    """Интерфейс шлюза оплаты."""
    
    def charge(self, order_id: str, amount: Money) -> str:
        """Провести платёж и вернуть ID транзакции."""
        ...

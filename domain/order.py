from dataclasses import dataclass, field
from typing import List

from .money import Money
from .order_line import OrderLine
from .order_status import OrderStatus


@dataclass
class Order:
    """Агрегат — заказ."""
    order_id: str
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.DRAFT
    total: Money = None

    def __post_init__(self):
        """Вычисляем итоговую сумму при создании."""
        self._recalculate_total()

    def add_line(self, line: OrderLine):
        """Добавляем строку — только если заказ не оплачен."""
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self.lines.append(line)
        self._recalculate_total()

    def pay(self):
        """Оплата заказа с проверкой инвариантов."""
        if self.status == OrderStatus.PAID:
            raise ValueError("Order is already paid")

        if not self.lines:
            raise ValueError("Cannot pay empty order")

        self.status = OrderStatus.PAID

    def _recalculate_total(self):
        """Пересчитываем общую сумму как сумму всех строк."""
        if not self.lines:
            self.total = Money(0)
            return

        total_amount = sum(line.total().amount for line in self.lines)
        currency = self.lines[0].price.currency  # все строки в одной валюте
        self.total = Money(total_amount, currency)

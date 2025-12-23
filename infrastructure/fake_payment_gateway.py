import uuid

from domain.money import Money
from application.interfaces import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """Фейковый шлюз оплаты — всегда успешно проводит платёж."""
    
    def __init__(self):
        self.charged_orders = []  # для тестов можно проверить, что вызвали

    def charge(self, order_id: str, amount: Money) -> str:
        """Имитирует успешный платёж и возвращает фейковый ID транзакции."""
        transaction_id = str(uuid.uuid4())
        self.charged_orders.append({
            "order_id": order_id,
            "amount": amount,
            "transaction_id": transaction_id
        })
        return transaction_id

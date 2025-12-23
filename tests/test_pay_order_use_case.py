import pytest

from domain.money import Money
from domain.order import Order
from domain.order_line import OrderLine
from domain.order_status import OrderStatus

from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


@pytest.fixture
def repository():
    return InMemoryOrderRepository()


@pytest.fixture
def gateway():
    return FakePaymentGateway()


@pytest.fixture
def use_case(repository, gateway):
    return PayOrderUseCase(order_repository=repository, payment_gateway=gateway)


def test_successful_payment(use_case, repository):
    # Создаём заказ с одной строкой
    order = Order(order_id="order-123")
    line = OrderLine(product_id="book", quantity=2, price=Money(1500))  # 15.00 USD
    order.add_line(line)

    # Сохраняем заказ в репозитории
    repository.save(order)

    # Выполняем оплату
    transaction_id = use_case.execute("order-123")

    # Проверяем результат
    paid_order = repository.get_by_id("order-123")
    assert paid_order.status == OrderStatus.PAID
    assert paid_order.total == Money(3000)  # 2 * 15.00
    assert transaction_id is not None
    assert gateway.charged_orders[-1]["order_id"] == "order-123"
    assert gateway.charged_orders[-1]["amount"] == Money(3000)


def test_cannot_pay_empty_order(use_case):
    order = Order(order_id="empty-order")
    repository = InMemoryOrderRepository()
    repository.save(order)

    with pytest.raises(ValueError, match="Cannot pay empty order"):
        use_case.execute("empty-order")


def test_cannot_pay_twice(use_case, repository):
    order = Order(order_id="order-456")
    line = OrderLine(product_id="pen", quantity=1, price=Money(500))
    order.add_line(line)
    repository.save(order)

    use_case.execute("order-456")  # первая оплата

    with pytest.raises(ValueError, match="Order is already paid"):
        use_case.execute("order-456")  # вторая попытка


def test_cannot_modify_after_payment(use_case, repository):
    order = Order(order_id="order-789")
    line = OrderLine(product_id="notebook", quantity=1, price=Money(2000))
    order.add_line(line)
    repository.save(order)

    use_case.execute("order-789")  # оплатили

    with pytest.raises(ValueError, match="Cannot modify paid order"):
        order.add_line(OrderLine(product_id="extra", quantity=1, price=Money(100)))


def test_total_is_always_correct(repository):
    order = Order(order_id="calc-order")
    order.add_line(OrderLine("item1", 2, Money(1000)))  # 20.00
    order.add_line(OrderLine("item2", 3, Money(500)))   # 15.00

    assert order.total == Money(3500)  # 35.00

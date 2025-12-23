from enum import StrEnum, auto


class OrderStatus(StrEnum):
    """Статусы заказа."""
    DRAFT = auto()      # черновик, ещё не оплачен
    PAID = auto()       # успешно оплачен
    CANCELLED = auto()  # отменён

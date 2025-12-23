# Лабораторная работа №7 — Архитектура, слои и DDD-lite

Реализация небольшой системы оплаты заказа с использованием слоистой архитектуры и основ Domain-Driven Design (DDD-lite).

## Структура проекта

- **domain/** — доменная модель:
  - `Money` — Value Object для денег
  - `OrderStatus` — перечисление статусов заказа
  - `OrderLine` — строка заказа
  - `Order` — агрегат с доменными инвариантами

- **application/** — слой применения:
  - `interfaces.py` — интерфейсы `OrderRepository` и `PaymentGateway`
  - `pay_order_use_case.py` — use-case оплаты заказа

- **infrastructure/** — реализации внешних зависимостей:
  - `in_memory_order_repository.py` — репозиторий в памяти# lab7-architecture-ddd

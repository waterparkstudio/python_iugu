from dataclasses import dataclass


@dataclass
class Data:
    holder_name: str
    display_number: str
    brand: str
    month: int
    year: int

@dataclass
class PaymentMethodModel:
    id: str
    description: str
    price_cents: int
    data: Data


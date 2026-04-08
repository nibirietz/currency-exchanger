from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Currency:
    id: int
    code: str
    full_name: str
    sign: str


@dataclass
class ExchangeRates:
    id: int
    base_currency_id: int
    target_currency_id: int
    rate: Decimal

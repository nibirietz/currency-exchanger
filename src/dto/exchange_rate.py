from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExchangeRate:
    rate: Decimal


@dataclass
class ExchangeRatePost(ExchangeRate):
    base_currency_id: int
    target_currency_id: int

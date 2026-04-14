from dataclasses import dataclass
from decimal import Decimal

from src.dto.currency_dto import Currency


@dataclass
class ExchangeRate:
    rate: Decimal


@dataclass
class ExchangeRateRequest(ExchangeRate):
    base_currency_code: str
    target_currency_code: str


@dataclass
class ExchangeRateResponse(ExchangeRate):
    id: int
    base_currency: Currency
    target_currency: Currency

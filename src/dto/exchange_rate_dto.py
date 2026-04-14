from dataclasses import dataclass
from decimal import Decimal

from src.dto.currency_dto import Currency


@dataclass
class ExchangeRate:
    rate: Decimal


@dataclass
class ExchangeRateRequest(ExchangeRate):
    base_currency_id: int
    target_currency_id: int


@dataclass
class ExchangeRateResponse(ExchangeRate):
    id: int
    base_currency: Currency
    target_currency: Currency

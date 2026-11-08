from dataclasses import dataclass
from decimal import Decimal

from src.dto.currency_dto import CurrencyResponse


@dataclass(frozen=True)
class ExchangeResponse:
    base_currency: CurrencyResponse
    target_currency: CurrencyResponse
    rate: Decimal
    amount: Decimal
    converted_rate: Decimal

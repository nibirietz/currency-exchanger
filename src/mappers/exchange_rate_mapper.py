import sqlite3
from dataclasses import asdict
from decimal import Decimal

from src.dto.currency_dto import CurrencyResponse
from src.dto.exchange_rate_dto import ExchangeRateResponse


class ExchangeRateMapper:
    @staticmethod
    def row_to_response(row: sqlite3.Row) -> ExchangeRateResponse:
        base_currency = CurrencyResponse(
            id=row["base_currency_id"],
            name=row["base_currency_full_name"],
            code=row["base_currency_code"],
            sign=row["base_currency_sign"]
        )

        target_currency = CurrencyResponse(
            id=row["target_currency_id"],
            name=row["target_currency_full_name"],
            code=row["target_currency_code"],
            sign=row["target_currency_sign"]
        )

        exchange_rate = ExchangeRateResponse(
            id=row["id"],
            base_currency=base_currency,
            target_currency=target_currency,
            rate=Decimal(row["rate"])
        )

        return exchange_rate

    @staticmethod
    def response_to_view(response: ExchangeRateResponse) -> dict:
        view = {
            "id": response.id,
            "base_currency": asdict(response.base_currency),
            "target_currency": asdict(response.target_currency),
            "rate": str(response.rate)
        }

        return view

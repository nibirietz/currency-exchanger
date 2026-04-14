import sqlite3
from dataclasses import asdict

from src.dto.currency_dto import CurrencyRequest, CurrencyResponse


class CurrencyMapper:
    @staticmethod
    def dict_to_request(currency: dict) -> CurrencyRequest:
        return CurrencyRequest(
            name=currency["name"],
            code=currency["code"],
            sign=currency["sign"]
        )

    @staticmethod
    def response_to_dict(currency: CurrencyResponse) -> dict:
        return asdict(currency)

    @staticmethod
    def row_to_response(row: sqlite3.Row) -> CurrencyResponse:
        return CurrencyResponse(
            id=row["id"],
            code=row["code"],
            name=row["full_name"],
            sign=row["sign"]
        )

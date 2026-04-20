import sqlite3
from decimal import Decimal

from src.database.exchange_rate_dao import ExchangeRateDAO
from src.dto.exchange_rate_dto import ExchangeRateResponse
from src.exceptions import (
    CurrencyNotFoundError,
    ExchangeRateAlreadyExistsError,
    ExchangeRateNotFoundError,
)


class ExchangeRateService:
    def __init__(self, exchange_rate_dao: ExchangeRateDAO):
        self.exchange_rate_dao = exchange_rate_dao

    def add_exchange_rate(
        self, base_currency_name: str, target_currency_name: str, rate: Decimal
    ) -> ExchangeRateResponse:
        try:
            inserted_id = self.exchange_rate_dao.add_exchange_rates(
                base_currency_name, target_currency_name, rate
            )
            if inserted_id == 0:
                raise CurrencyNotFoundError(
                    "Одна(или обе) валюта из валютной пары не существует."
                )
        except sqlite3.IntegrityError:
            raise ExchangeRateAlreadyExistsError("Валютная пара уже существует.")

        return self.exchange_rate_dao.get_exchange_rate_by_id(inserted_id)

    def get_all_exchange_rates(self) -> list[ExchangeRateResponse]:
        exchange_rates: list[ExchangeRateResponse] = (
            self.exchange_rate_dao.get_all_exchange_rates()
        )
        return exchange_rates

    def get_exchange_rate(
        self, base_code: str, target_code: str
    ) -> ExchangeRateResponse:
        exchange_rate = self.exchange_rate_dao.get_exchange_rate(base_code, target_code)
        if not exchange_rate:
            raise ExchangeRateNotFoundError("Обменный курс не найден.")

        return exchange_rate

    def patch_exchange_rate(
        self, base_code: str, target_code: str, rate: Decimal
    ) -> ExchangeRateResponse:
        self.exchange_rate_dao.patch_exchange_rate(base_code, target_code, rate)
        exchange_rate = self.exchange_rate_dao.get_exchange_rate(base_code, target_code)
        if not exchange_rate:
            raise ExchangeRateNotFoundError("Обменный курс не найден.")

        return exchange_rate

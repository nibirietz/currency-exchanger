import json
from decimal import Decimal

from src.database.currency_dao import CurrencyDAO
from src.database.exchange_rate_dao import ExchangeRateDAO
from src.exceptions import ExchangeRateNotFoundError, CurrencyNotFoundError
from src.mappers.currency_mapper import CurrencyMapper
from src.mappers.exchange_mapper import ExchangeMapper
from src.mappers.exchange_rate_mapper import ExchangeRateMapper


class ExchangeService:
    def __init__(self, currency_dao: CurrencyDAO, exchange_rate_dao: ExchangeRateDAO):
        self.currency_dao = currency_dao
        self.exchange_rate_dao = exchange_rate_dao

    def get_exchange(self, base_code: str, target_code: str, amount: Decimal) -> dict:
        exchange_rate = self.exchange_rate_dao.get_exchange_rate(base_code, target_code)

        if exchange_rate:
            converted_amount = amount * exchange_rate.rate
            exchange = ExchangeMapper.exchange_rate_to_dict(exchange_rate, amount, converted_amount)
            return exchange
        else:
            exchange_rate = self.exchange_rate_dao.get_exchange_rate(target_code, base_code)
            if exchange_rate:
                converted_amount = amount / exchange_rate.rate
                exchange = ExchangeMapper.exchange_rate_to_dict(exchange_rate, amount, converted_amount)

                return exchange
            else:
                exchange_rate_usd_to_base = self.exchange_rate_dao.get_exchange_rate("USD", base_code)
                exchange_rate_usd_to_target = self.exchange_rate_dao.get_exchange_rate("USD", target_code)

                if exchange_rate_usd_to_base and exchange_rate_usd_to_target:
                    base_currency = self.currency_dao.get_currency(base_code)
                    target_currency = self.currency_dao.get_currency(target_code)
                    rate = exchange_rate_usd_to_target.rate / exchange_rate_usd_to_base.rate
                    converted_amount = amount * rate
                    if base_currency and target_currency:
                        exchange = ExchangeMapper.currencies_to_dict(base_currency, target_currency, rate, amount,
                                                                     converted_amount)
                        print(exchange)
                        return exchange
                    else:
                        raise CurrencyNotFoundError("Валюта не найдена.")

                else:
                    raise ExchangeRateNotFoundError("Обменная пара не найдена")

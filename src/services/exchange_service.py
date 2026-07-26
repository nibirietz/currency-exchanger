from decimal import Decimal

from src.database.currency_dao import CurrencyDAO
from src.database.exchange_rate_dao import ExchangeRateDAO
from src.exceptions import ExchangeRateNotFoundError
from src.mappers.exchange_mapper import ExchangeMapper


class ExchangeService:
    def __init__(self, currency_dao: CurrencyDAO, exchange_rate_dao: ExchangeRateDAO):
        self.currency_dao = currency_dao
        self.exchange_rate_dao = exchange_rate_dao

    def _get_direct_rate(self, base_code: str, target_code: str, amount: Decimal) -> dict | None:
        exchange_rate = self.exchange_rate_dao.get_exchange_rate(base_code, target_code)

        if exchange_rate is not None:
            converted_amount = amount * exchange_rate.rate
            exchange = ExchangeMapper.exchange_rate_to_dict(exchange_rate, amount, converted_amount)
            return exchange

        return None

    def _get_reverse_rate(self, base_code: str, target_code: str, amount: Decimal) -> dict | None:
        exchange_rate = self.exchange_rate_dao.get_exchange_rate(target_code, base_code)

        if exchange_rate is not None:
            rate = exchange_rate.rate
            converted_amount = amount / rate
            base_currency = self.currency_dao.get_currency(base_code)
            target_currency = self.currency_dao.get_currency(target_code)
            if base_currency is not None and target_currency is not None:
                exchange = ExchangeMapper.currencies_to_dict(base_currency, target_currency, 1 / rate, amount,
                                                             converted_amount)

                return exchange

        return None

    def _get_cross_rate(self, base_code: str, target_code: str, amount: Decimal) -> dict | None:
        exchange_rate_usd_to_base = self.exchange_rate_dao.get_exchange_rate("USD", base_code)
        exchange_rate_usd_to_target = self.exchange_rate_dao.get_exchange_rate("USD", target_code)

        if exchange_rate_usd_to_base is not None and exchange_rate_usd_to_target is not None:
            base_currency = self.currency_dao.get_currency(base_code)
            target_currency = self.currency_dao.get_currency(target_code)
            rate = exchange_rate_usd_to_target.rate / exchange_rate_usd_to_base.rate
            converted_amount = amount * rate
            if base_currency is not None and target_currency is not None:
                exchange = ExchangeMapper.currencies_to_dict(base_currency, target_currency, rate, amount,
                                                             converted_amount)
                return exchange
            else:
                return None
        else:
            raise ExchangeRateNotFoundError("Обменная пара не найдена")

    def get_exchange(self, base_code: str, target_code: str, amount: Decimal) -> dict:
        exchange = self._get_direct_rate(base_code, target_code, amount)
        if exchange is not None:
            return exchange

        exchange = self._get_reverse_rate(base_code, target_code, amount)
        if exchange is not None:
            return exchange

        exchange = self._get_cross_rate(base_code, target_code, amount)
        if exchange is not None:
            return exchange

        raise ExchangeRateNotFoundError("Обменная пара не найдена.")

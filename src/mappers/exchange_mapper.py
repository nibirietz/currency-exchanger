from decimal import Decimal

from src.dto.currency_dto import CurrencyResponse
from src.dto.exchange_rate_dto import ExchangeRateResponse
from src.mappers.currency_mapper import CurrencyMapper


class ExchangeMapper:
    @staticmethod
    def exchange_rate_to_dict(exchange_rate: ExchangeRateResponse,
                              amount: Decimal, converted_amount: Decimal) -> dict:
        base_currency = exchange_rate.base_currency
        target_currency = exchange_rate.target_currency
        return {
            "baseCurrency": {
                "id": base_currency.id,
                "name": base_currency.name,
                "code": base_currency.code,
                "sign": base_currency.sign
            },
            "targetCurrency": {
                "id": target_currency.id,
                "name": target_currency.name,
                "code": target_currency.code,
                "sign": target_currency.sign
            },
            "rate": float(exchange_rate.rate),
            "amount": float(amount),
            "convertedAmount": float(converted_amount)
        }

    @staticmethod
    def currencies_to_dict(base_currency: CurrencyResponse, target_currency: CurrencyResponse, rate: Decimal,
                           amount: Decimal, converted_amount: Decimal) -> dict:
        return {
            "baseCurrency": CurrencyMapper.response_to_dict(base_currency),
            "targetCurrency": CurrencyMapper.response_to_dict(target_currency),
            "rate": float(rate),
            "amount": float(amount),
            "convertedAmount": float(converted_amount)
        }

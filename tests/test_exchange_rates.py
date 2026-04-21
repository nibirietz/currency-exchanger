from decimal import Decimal
import requests
from tests.conftest import assert_currencies_response


def test_get_exchange_rates_returns_200(server_url, currency_dao, exchange_rate_dao, currency_factory):
    currency1 = currency_factory(code="USD")
    currency2 = currency_factory(code="RUB")
    currency1_id = currency_dao.add_currency(**currency1)
    currency2_id = currency_dao.add_currency(**currency2)
    exchange_rate_id = exchange_rate_dao.add_exchange_rate_by_id(currency1_id, currency2_id, Decimal("0.5"))

    response = requests.get(f"{server_url}/exchangeRate/USDRUB", timeout=3)
    assert response.status_code == 200
    response_data = response.json()

    assert response_data["id"] == exchange_rate_id

    assert_currencies_response(response_data["baseCurrency"], currency1)
    assert_currencies_response(response_data["targetCurrency"], currency2)

    assert response_data["rate"] == "0.5"


def test_add_exchange_rate_returns_201(server_url, exchange_rate_dao, currency_dao, currency_factory):
    currency1 = currency_factory(code="USD")
    currency2 = currency_factory(code="RUB")
    currency_dao.add_currency(**currency1)
    currency_dao.add_currency(**currency2)
    rate = Decimal("0.5")

    data = {
        "baseCurrencyCode": currency1["code"],
        "targetCurrencyCode": currency2["code"],
        "rate": str(rate)
    }

    response = requests.post(f"{server_url}/exchangeRates", data=data, timeout=3)
    assert response.status_code == 201
    response_data = response.json()

    assert_currencies_response(response_data["baseCurrency"], currency1)
    assert_currencies_response(response_data["targetCurrency"], currency2)

    currency1_db = currency_dao.get_currency(response_data["baseCurrency"]["code"])
    currency2_db = currency_dao.get_currency(response_data["targetCurrency"]["code"])

    assert currency1_db is not None
    assert currency2_db is not None

    exchange_rate = exchange_rate_dao.get_exchange_rate_by_id(response_data["id"])
    assert response_data["baseCurrency"]["id"] == exchange_rate.base_currency.id
    assert response_data["targetCurrency"]["id"] == exchange_rate.target_currency.id

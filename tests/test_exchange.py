from collections.abc import Callable, Mapping
from decimal import Decimal
from pathlib import Path

import pytest
import requests

from src.database.currency_dao import CurrencyDAO
from src.database.exchange_rate_dao import ExchangeRateDAO
from tests.conftest import create_currency


@pytest.mark.parametrize(
    "frm,to,excepted", [("RUB", "EUR", Decimal(1)), ("EUR", "RUB", Decimal(4))]
)
def test_get_exchange_returns_200(
    server_url: Path,
    exchange_rate_dao: ExchangeRateDAO,
    currency_dao: CurrencyDAO,
    frm: str,
    to: str,
    excepted: Decimal,
):
    currency1 = create_currency(code="RUB")
    currency2 = create_currency(code="EUR")
    _ = currency_dao.add_currency(**currency1)
    _ = currency_dao.add_currency(**currency2)
    rate = Decimal("0.5")
    amount = 2
    _ = exchange_rate_dao.add_exchange_rates(currency1["code"], currency2["code"], rate)

    payload = {"from": frm, "to": to, "amount": amount}

    response = requests.get(f"{server_url}/exchange", params=payload)
    assert response.status_code == 200
    response_data = response.json()

    assert Decimal(response_data["convertedAmount"]) == excepted
    assert response_data["baseCurrency"]["code"] == frm
    assert response_data["targetCurrency"]["code"] == to


def test_get_exchange_from_a_to_usd_to_b_returns_200(
    server_url: Path,
    exchange_rate_dao: ExchangeRateDAO,
    currency_dao: CurrencyDAO,
):
    currency1 = create_currency(code="USD")
    currency2 = create_currency(code="EUR")
    currency3 = create_currency(code="RUB")
    _ = currency_dao.add_currency(**currency1)
    _ = currency_dao.add_currency(**currency2)
    _ = currency_dao.add_currency(**currency3)
    rate1_to_2 = Decimal("0.5")
    rate1_to_3 = Decimal(2)
    amount = 10
    _ = exchange_rate_dao.add_exchange_rates(
        currency1["code"], currency2["code"], rate1_to_2
    )
    _ = exchange_rate_dao.add_exchange_rates(
        currency1["code"], currency3["code"], rate1_to_3
    )

    payload = {"from": currency2["code"], "to": currency3["code"], "amount": amount}

    response = requests.get(f"{server_url}/exchange", params=payload)
    assert response.status_code == 200
    response_data = response.json()

    assert Decimal(response_data["convertedAmount"]) == Decimal(40)
    assert response_data["baseCurrency"]["code"] == currency2["code"]
    assert response_data["targetCurrency"]["code"] == currency3["code"]


def test_get_exchange_from_a_to_a_returns_200(
    server_url: Path,
    currency_dao: CurrencyDAO,
):
    currency = create_currency(code="USD")
    amount = 100
    currency_dao.add_currency(currency["code"], currency["name"], currency["sign"])

    payload = {"from": currency["code"], "to": currency["code"], "amount": amount}

    response = requests.get(f"{server_url}/exchange", params=payload)
    assert response.status_code == 200
    response_data = response.json()

    assert Decimal(response_data["convertedAmount"]) == Decimal(100)
    assert response_data["baseCurrency"]["code"] == currency["code"]
    assert response_data["targetCurrency"]["code"] == currency["code"]


def test_get_exchange_with_non_existent_return_404(
    server_url: Path,
    currency_dao: CurrencyDAO,
):
    currency1 = create_currency(code="USD")
    currency2 = create_currency(code="RUB")
    amount = 100
    currency_dao.add_currency(currency1["code"], currency1["name"], currency1["sign"])
    currency_dao.add_currency(currency2["code"], currency2["name"], currency2["sign"])

    payload = {"from": currency1["code"], "to": currency2["code"], "amount": amount}

    response = requests.get(f"{server_url}/exchange", params=payload)
    assert response.status_code == 404
    assert "message" in response.json()

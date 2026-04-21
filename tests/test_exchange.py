from decimal import Decimal

import pytest
import requests


@pytest.mark.parametrize("frm,to,excepted", [("RUB", "EUR", 10), ("EUR", "RUB", 40)])
def test_get_exchange_returns_200(server_url, exchange_rate_dao, currency_dao, currency_factory,
                                  frm, to, excepted):
    currency1 = currency_factory(code="RUB")
    currency2 = currency_factory(code="EUR")
    currency1_id = currency_dao.add_currency(**currency1)
    currency2_id = currency_dao.add_currency(**currency2)
    rate = Decimal("0.5")
    amount = 20
    exchange_rate_dao.add_exchange_rate_by_id(currency1_id, currency2_id, rate)

    payload = {
        "from": frm,
        "to": to,
        "amount": amount
    }

    response = requests.get(f"{server_url}/exchange", params=payload)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)

    assert response_data["convertedAmount"] == excepted
    assert response_data["baseCurrency"]["code"] == currency1["code"]
    assert response_data["targetCurrency"]["code"] == currency2["code"]


def test_get_exchange_from_a_to_usd_to_b_returns_200(server_url, exchange_rate_dao, currency_dao, currency_factory):
    currency1 = currency_factory(code="USD")
    currency2 = currency_factory(code="EUR")
    currency3 = currency_factory(code="RUB")
    currency1_id = currency_dao.add_currency(**currency1)
    currency2_id = currency_dao.add_currency(**currency2)
    currency3_id = currency_dao.add_currency(**currency3)
    rate1_to_2 = Decimal("0.5")
    rate1_to_3 = Decimal("2")
    amount = 10
    exchange_rate_dao.add_exchange_rate_by_id(currency1_id, currency2_id, rate1_to_2)
    exchange_rate_dao.add_exchange_rate_by_id(currency1_id, currency3_id, rate1_to_3)

    payload = {
        "from": currency2["code"],
        "to": currency3["code"],
        "amount": amount
    }

    response = requests.get(f"{server_url}/exchange", params=payload)
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)

    assert response_data["convertedAmount"] == 40
    assert response_data["baseCurrency"]["code"] == currency2["code"]
    assert response_data["targetCurrency"]["code"] == currency3["code"]

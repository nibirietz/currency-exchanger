from dataclasses import asdict
from pathlib import Path

import pytest
import requests
from src.database.currency_dao import CurrencyDAO
from tests.conftest import create_currency

from tests.conftest import assert_currencies_response


def test_get_currencies_returns_200(server_url: Path, currency_dao: CurrencyDAO):
    currency1 = create_currency(code="USD")
    currency2 = create_currency(code="RUB")
    currency1_id = currency_dao.add_currency(**currency1)
    currency2_id = currency_dao.add_currency(**currency2)

    response = requests.get(f"{server_url}/currencies")

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)
    currency1_response = response_data[0]
    currency2_response = response_data[1]

    assert currency1_id == currency1_response["id"]
    assert_currencies_response(currency1, currency1_response)

    assert currency2_id == currency2_response["id"]
    assert_currencies_response(currency2, currency2_response)


def test_get_currency_returns_200(server_url: Path, currency_dao: CurrencyDAO):
    currency = create_currency(code="USD")
    currency_id = currency_dao.add_currency(**currency)

    response = requests.get(f"{server_url}/currency/USD")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == currency_id
    assert_currencies_response(response_data, currency)


def test_get_missing_currency_404(server_url: Path):
    response = requests.get(f"{server_url}/currency/USD")

    assert response.status_code == 404


def test_get_currency_without_code_400(server_url: Path):
    response = requests.get(f"{server_url}/currency")

    assert response.status_code == 400


def test_add_currency_returns_201(server_url: Path, currency_dao: CurrencyDAO):
    currency = create_currency(code="USD")

    response = requests.post(
        f"{server_url}/currencies",
        data=currency,
    )
    assert response.status_code == 201

    response_data = response.json()

    assert isinstance(response_data["id"], int)
    assert_currencies_response(currency, response_data)

    currency_db = currency_dao.get_currency("USD")
    assert currency_db is not None
    assert currency_db.id == response_data["id"]
    assert_currencies_response(currency, asdict(currency_db))


@pytest.mark.parametrize("empty_field", ["code", "name", "sign"])
def test_add_currency_with_empty_field_returns_400(
    empty_field, server_url: Path, currency_dao: CurrencyDAO
):
    data = create_currency(code="USD")
    data[empty_field] = ""

    response = requests.post(
        f"{server_url}/currencies",
        data=data,
        timeout=3,
    )
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("USD") is None


@pytest.mark.parametrize("without", ["code", "name", "sign"])
def test_add_currency_without_required_field_returns_400(
    without, server_url: Path, currency_dao: CurrencyDAO
):
    data = create_currency(code="USD", without=[without])

    response = requests.post(
        f"{server_url}/currencies",
        data=data,
        timeout=3,
    )
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("USD") is None


def test_add_already_exists_currency_returns_409(
    server_url: Path, currency_dao: CurrencyDAO
):
    data = create_currency(code="USD")

    currency_dao.add_currency("USD", "United States dollar", "$")

    response = requests.post(
        f"{server_url}/currencies",
        data=data,
        timeout=3,
    )
    assert response.status_code == 409
    response_data = response.json()

    assert "message" in response_data


@pytest.mark.parametrize("code", ["US", "USDT"])
def test_add_currency_with_invalid_code_length_400(
    server_url: Path, currency_dao: CurrencyDAO, code: str
):
    data = create_currency(code="USD")
    data["code"] = code

    response = requests.post(
        f"{server_url}/currencies",
        data=data,
        timeout=3,
    )
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("US") is None


def test_add_currency_with_invalid_sign_length_400(
    server_url: Path, currency_dao: CurrencyDAO
):
    data = create_currency(code="USD")
    data["sign"] = "$$$$"

    response = requests.post(
        f"{server_url}/currencies",
        data=data,
        timeout=3,
    )
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("USD") is None

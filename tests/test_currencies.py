from dataclasses import asdict

import pytest
import requests

from tests.conftest import assert_currencies_response


def test_get_currencies_returns_200(server_url, currency_dao, currency_factory):
    currency1 = currency_factory(code="USD")
    currency2 = currency_factory(code="RUB")
    currency1_id = currency_dao.add_currency(**currency1)
    currency2_id = currency_dao.add_currency(**currency2)

    response = requests.get(f"{server_url}/currencies", timeout=3)

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)
    currency1_response = response_data[0]
    currency2_response = response_data[1]

    assert currency1_id == currency1_response["id"]
    assert_currencies_response(currency1, currency1_response)

    assert currency2_id == currency2_response["id"]
    assert_currencies_response(currency2, currency2_response)


def test_get_currency_returns_200(server_url, currency_dao, currency_factory):
    currency = currency_factory(code="USD")
    currency_id = currency_dao.add_currency(**currency)

    response = requests.get(f"{server_url}/currency/USD")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == currency_id
    assert_currencies_response(response_data, currency)


def test_get_missing_currency_404(server_url):
    response = requests.get(f"{server_url}/currency/USD")

    assert response.status_code == 404


def test_get_currency_without_code_400(server_url):
    response = requests.get(f"{server_url}/currency")

    assert response.status_code == 400


def test_add_currency_returns_201(server_url, currency_dao, currency_factory):
    data = currency_factory(code="USD")

    response = requests.post(f"{server_url}/currencies", data=data)
    assert response.status_code == 201

    response_data = response.json()

    assert isinstance(response_data["id"], int)
    assert response_data["code"] == "USD"
    assert response_data["name"] == "United States dollar"
    assert response_data["sign"] == "$"

    currency = currency_dao.get_currency("USD")
    assert currency is not None
    assert currency.id == response_data["id"]
    assert_currencies_response(data, asdict(currency))


@pytest.mark.parametrize("without", ["code", "name", "sign"])
def test_add_currency_without_required_field_returns_400(without, server_url, currency_dao, currency_factory):
    data = currency_factory(code="USD", without=[without])

    response = requests.post(f"{server_url}/currencies", data=data)
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("USD") is None


def test_add_already_exists_currency_returns_409(server_url, currency_dao, currency_factory):
    data = currency_factory(code="USD")

    currency_dao.add_currency("USD", "United States dollar", "$")

    response = requests.post(f"{server_url}/currencies", data=data)
    assert response.status_code == 409
    response_data = response.json()

    assert "message" in response_data


def test_add_currency_with_invalid_code_length_400(server_url, currency_dao, currency_factory):
    data = currency_factory(code="USD")
    data["code"] = "US"

    response = requests.post(f"{server_url}/currencies", data=data)
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("US") is None


def test_add_currency_with_invalid_sign_length_400(server_url, currency_dao, currency_factory):
    data = currency_factory(code="USD")
    data["sign"] = "$$$$"

    response = requests.post(f"{server_url}/currencies", data=data)
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("USD") is None

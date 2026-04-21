import requests


def test_get_currencies_returns_202(server_url, currency_dao):
    currency1_id = currency_dao.add_currency("USD", "United States dollar", "$")
    currency2_id = currency_dao.add_currency("RUB", "Russian ruble", "₽")

    response = requests.get(f"{server_url}/currencies")

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)
    currency1 = response_data[0]
    currency2 = response_data[1]

    assert currency1["id"] == currency1_id
    assert currency1["code"] == "USD"
    assert currency1["sign"] == "$"
    assert currency1["name"] == "United States dollar"

    assert currency2["id"] == currency2_id
    assert currency2["code"] == "RUB"
    assert currency2["sign"] == "₽"
    assert currency2["name"] == "Russian ruble"


def test_get_currency_returns_200(server_url, currency_dao):
    currency_id = currency_dao.add_currency("USD", "United States dollar", "$")

    response = requests.get(f"{server_url}/currency/USD")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == currency_id
    assert response_data["code"] == "USD"
    assert response_data["sign"] == "$"
    assert response_data["name"] == "United States dollar"


def test_get_non_exists_currency_404(server_url):
    response = requests.get(f"{server_url}/currency/USD")

    assert response.status_code == 404


def test_get_currency_without_code_400(server_url):
    response = requests.get(f"{server_url}/currency")

    assert response.status_code == 400


def test_add_currency_returns_201(server_url, currency_dao):
    data = {
        "code": "USD",
        "name": "United States dollar",
        "sign": "$"
    }

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
    assert currency.code == "USD"
    assert currency.name == "United States dollar"
    assert currency.sign == "$"


def test_add_currency_without_required_field_returns_400(server_url, currency_dao):
    data = {
        "code": "USD",
        "name": "United States dollar"
    }

    response = requests.post(f"{server_url}/currencies", data=data)
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("USD") is None


def test_add_already_exists_currency_returns_409(server_url, currency_dao):
    data = {
        "code": "USD",
        "name": "United States dollar",
        "sign": "$"
    }

    currency_dao.add_currency("USD", "United States dollar", "$")

    response = requests.post(f"{server_url}/currencies", data=data)
    assert response.status_code == 409
    response_data = response.json()

    assert "message" in response_data


def test_add_currency_with_invalid_code_length_400(server_url, currency_dao):
    data = {
        "code": "XD",
        "name": "United States dollar",
        "sign": "$"
    }

    response = requests.post(f"{server_url}/currencies", data=data)
    assert response.status_code == 400
    response_data = response.json()

    assert "message" in response_data

    assert currency_dao.get_currency("XD") is None

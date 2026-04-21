import requests


def test_get_currency_return_200(server_url, currency_dao):
    currency_id = currency_dao.add_currency("USD", "United States dollar", "$")

    response = requests.get(f"{server_url}/currency/USD")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == currency_id
    assert response_data["code"] == "USD"
    assert response_data["sign"] == "$"
    assert response_data["name"] == "United States dollar"


def test_add_currency_return_201(server_url, currency_dao):
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

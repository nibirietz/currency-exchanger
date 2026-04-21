import requests


def test_add_currency_return_201(server_url):
    data = {
        "code": "USD",
        "name": "United States dollar",
        "sign": "$"
    }

    response = requests.post(f"{server_url}/currencies", data)
    assert response.status_code == 201

    response_data = response.json()
    print(response_data)

    assert isinstance(response_data["id"], int)
    assert response_data["code"] == "USD"
    assert response_data["name"] == "United States dollar"
    assert response_data["sign"] == "$"

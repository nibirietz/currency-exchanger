def test_get_currencies_returns_200_and_list(http, base_url):
    response = http.get(f"{base_url}/currencies")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        currency = data[0]
        assert isinstance(currency["id"], int)
        assert isinstance(currency["name"], str)
        assert isinstance(currency["code"], str)
        assert isinstance(currency["sign"], str)
        assert len(currency["code"]) == 3
        assert currency["code"].isalpha()
        assert currency["code"].isupper()


def test_get_currency_by_code_returns_200(http, base_url, ensure_currency):
    ensure_currency("CHF", "Swiss franc", "Fr")

    response = http.get(f"{base_url}/currency/CHF")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["name"] == "Swiss franc"
    assert data["code"] == "CHF"
    assert data["sign"] == "Fr"


def test_get_currency_with_unknown_code_returns_404(http, base_url):
    response = http.get(f"{base_url}/currency/ZZZ")

    assert response.status_code == 404

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_currency_returns_201_and_entity(http, base_url, currency_factory):
    created = currency_factory(preferred="SEK")
    response = created["response"]

    if response.request.method == "GET":
        created = currency_factory()
        response = created["response"]

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["name"] == created["name"]
    assert data["code"] == created["code"]
    assert data["sign"] == created["sign"]
    assert len(data["code"]) == 3
    assert data["code"].isalpha()
    assert data["code"].isupper()


def test_create_currency_without_name_returns_400(http, base_url):
    response = http.post(
        f"{base_url}/currencies",
        data={
            "code": "NOK",
            "sign": "kr",
        },
    )

    assert response.status_code == 400

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_currency_without_code_returns_400(http, base_url):
    response = http.post(
        f"{base_url}/currencies",
        data={
            "name": "Norwegian krone",
            "sign": "kr",
        },
    )

    assert response.status_code == 400

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_currency_without_sign_returns_400(http, base_url):
    response = http.post(
        f"{base_url}/currencies",
        data={
            "name": "Norwegian krone",
            "code": "NOK",
        },
    )

    assert response.status_code == 400

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_currency_with_duplicate_code_returns_409(http, base_url, ensure_currency):
    ensure_currency("JPY", "Japanese yen", "¥")

    response = http.post(
        f"{base_url}/currencies",
        data={
            "name": "Another yen",
            "code": "JPY",
            "sign": "¥",
        },
    )

    assert response.status_code == 409

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]

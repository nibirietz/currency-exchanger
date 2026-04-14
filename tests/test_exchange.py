def test_get_exchange_rates_returns_200_and_list(http, base_url):
    response = http.get(f"{base_url}/exchangeRates")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        rate = data[0]
        assert isinstance(rate["id"], int)
        assert "baseCurrency" in rate
        assert "targetCurrency" in rate
        assert "rate" in rate

        assert len(rate["baseCurrency"]["code"]) == 3
        assert rate["baseCurrency"]["code"].isalpha()
        assert rate["baseCurrency"]["code"].isupper()

        assert len(rate["targetCurrency"]["code"]) == 3
        assert rate["targetCurrency"]["code"].isalpha()
        assert rate["targetCurrency"]["code"].isupper()


def test_get_exchange_rate_by_pair_returns_200(http, base_url, ensure_rate):
    ensure_rate(
        "USD", "United States dollar", "$",
        "EUR", "Euro", "€",
        "0.91",
    )

    response = http.get(f"{base_url}/exchangeRate/USDEUR")

    assert response.status_code == 200

    data = response.json()
    assert data["baseCurrency"]["code"] == "USD"
    assert data["targetCurrency"]["code"] == "EUR"
    assert float(data["rate"]) == 0.91


def test_get_exchange_rate_with_unknown_pair_returns_404(http, base_url):
    response = http.get(f"{base_url}/exchangeRate/ZZZYYY")

    assert response.status_code == 404

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_exchange_rate_returns_201_and_entity(http, base_url, ensure_currency):
    ensure_currency("AUD", "Australian dollar", "A$")
    ensure_currency("CAD", "Canadian dollar", "C$")

    response = http.post(
        f"{base_url}/exchangeRates",
        data={
            "baseCurrencyCode": "AUD",
            "targetCurrencyCode": "CAD",
            "rate": "0.89",
        },
    )

    if response.status_code == 409:
        response = http.post(
            f"{base_url}/exchangeRates",
            data={
                "baseCurrencyCode": "CAD",
                "targetCurrencyCode": "AUD",
                "rate": "1.12",
            },
        )

    assert response.status_code == 201

    data = response.json()
    assert data["baseCurrency"]["code"] in ("AUD", "CAD")
    assert data["targetCurrency"]["code"] in ("CAD", "AUD")
    assert isinstance(data["id"], int)
    assert "rate" in data


def test_create_exchange_rate_without_base_currency_code_returns_400(http, base_url):
    response = http.post(
        f"{base_url}/exchangeRates",
        data={
            "targetCurrencyCode": "EUR",
            "rate": "0.91",
        },
    )

    assert response.status_code == 400

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_exchange_rate_without_target_currency_code_returns_400(http, base_url):
    response = http.post(
        f"{base_url}/exchangeRates",
        data={
            "baseCurrencyCode": "USD",
            "rate": "0.91",
        },
    )

    assert response.status_code == 400

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_exchange_rate_without_rate_returns_400(http, base_url):
    response = http.post(
        f"{base_url}/exchangeRates",
        data={
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "EUR",
        },
    )

    assert response.status_code == 400

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_exchange_rate_with_unknown_currency_returns_404(http, base_url):
    response = http.post(
        f"{base_url}/exchangeRates",
        data={
            "baseCurrencyCode": "ZZZ",
            "targetCurrencyCode": "YYY",
            "rate": "1.23",
        },
    )

    assert response.status_code == 404

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_create_exchange_rate_with_duplicate_pair_returns_409(http, base_url, ensure_rate):
    ensure_rate(
        "GBP", "Pound sterling", "£",
        "JPY", "Japanese yen", "¥",
        "188.50",
    )

    response = http.post(
        f"{base_url}/exchangeRates",
        data={
            "baseCurrencyCode": "GBP",
            "targetCurrencyCode": "JPY",
            "rate": "190.00",
        },
    )

    assert response.status_code == 409

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_patch_exchange_rate_returns_200_and_updated_entity(http, base_url, ensure_rate):
    ensure_rate(
        "USD", "United States dollar", "$",
        "RUB", "Russian ruble", "₽",
        "92.30",
    )

    response = http.patch(
        f"{base_url}/exchangeRate/USDRUB",
        data={"rate": "95.10"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["baseCurrency"]["code"] == "USD"
    assert data["targetCurrency"]["code"] == "RUB"
    assert float(data["rate"]) == 95.10


def test_patch_exchange_rate_without_rate_returns_400(http, base_url):
    response = http.patch(
        f"{base_url}/exchangeRate/USDRUB",
        data={},
    )

    assert response.status_code == 400

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]


def test_patch_exchange_rate_for_unknown_pair_returns_404(http, base_url):
    response = http.patch(
        f"{base_url}/exchangeRate/PLNMXN",
        data={"rate": "4.25"},
    )

    assert response.status_code == 404

    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"]

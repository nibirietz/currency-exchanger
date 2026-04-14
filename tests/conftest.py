"""ЭТОТ ФАЙЛ ПОЛНОСТЬЮ НАВАЙБКОЖЕН. КАК И ВСЕ ФАЙЛЫ В ПАПКЕ ТЕСТ. ПРОШУ НЕ ОСУЖДАТЬ, ТЕСТЫ ПОКА НЕ НАУЧИЛСЯ ПИСАТ."""

import os
from decimal import Decimal

import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8080")

REALISTIC_CURRENCIES = [
    ("USD", "United States dollar", "$"),
    ("EUR", "Euro", "€"),
    ("GBP", "Pound sterling", "£"),
    ("JPY", "Japanese yen", "¥"),
    ("CHF", "Swiss franc", "Fr"),
    ("AUD", "Australian dollar", "A$"),
    ("CAD", "Canadian dollar", "C$"),
    ("SEK", "Swedish krona", "kr"),
    ("NOK", "Norwegian krone", "kr"),
    ("DKK", "Danish krone", "kr"),
    ("PLN", "Polish zloty", "zł"),
    ("CZK", "Czech koruna", "Kč"),
    ("HUF", "Hungarian forint", "Ft"),
    ("CNY", "Chinese yuan", "¥"),
    ("HKD", "Hong Kong dollar", "HK$"),
    ("SGD", "Singapore dollar", "S$"),
    ("NZD", "New Zealand dollar", "NZ$"),
    ("RUB", "Russian ruble", "₽"),
    ("KZT", "Kazakhstani tenge", "₸"),
    ("UAH", "Ukrainian hryvnia", "₴"),
    ("TRY", "Turkish lira", "₺"),
    ("INR", "Indian rupee", "₹"),
    ("BRL", "Brazilian real", "R$"),
    ("ZAR", "South African rand", "R"),
    ("MXN", "Mexican peso", "$"),
]


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def http():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


@pytest.fixture
def currency_factory(http, base_url):
    used_codes = set()

    def _create(preferred=None):
        candidates = REALISTIC_CURRENCIES
        if preferred is not None:
            candidates = [item for item in REALISTIC_CURRENCIES if item[0] == preferred] + [
                item for item in REALISTIC_CURRENCIES if item[0] != preferred
            ]

        for code, name, sign in candidates:
            if code in used_codes:
                continue

            response = http.post(
                f"{base_url}/currencies",
                data={
                    "name": name,
                    "code": code,
                    "sign": sign,
                },
            )

            if response.status_code == 201:
                used_codes.add(code)
                return {
                    "response": response,
                    "code": code,
                    "name": name,
                    "sign": sign,
                }

            if response.status_code == 409:
                get_response = http.get(f"{base_url}/currency/{code}")
                if get_response.status_code == 200:
                    used_codes.add(code)
                    return {
                        "response": get_response,
                        "code": code,
                        "name": name,
                        "sign": sign,
                    }

        raise AssertionError("No realistic 3-letter currency codes left in test pool.")

    return _create


@pytest.fixture
def ensure_currency(http, base_url):
    def _ensure(code, name, sign):
        response = http.post(
            f"{base_url}/currencies",
            data={
                "name": name,
                "code": code,
                "sign": sign,
            },
        )

        if response.status_code == 201:
            return response

        if response.status_code == 409:
            return http.get(f"{base_url}/currency/{code}")

        return response

    return _ensure


@pytest.fixture
def ensure_rate(http, base_url, ensure_currency):
    def _ensure(
            base_code,
            base_name,
            base_sign,
            target_code,
            target_name,
            target_sign,
            rate,
    ):
        ensure_currency(base_code, base_name, base_sign)
        ensure_currency(target_code, target_name, target_sign)

        response = http.post(
            f"{base_url}/exchangeRates",
            data={
                "baseCurrencyCode": base_code,
                "targetCurrencyCode": target_code,
                "rate": str(rate),
            },
        )

        if response.status_code == 201:
            return response

        if response.status_code == 409:
            return http.patch(
                f"{base_url}/exchangeRate/{base_code}{target_code}",
                data={"rate": str(rate)},
            )

        return response

    return _ensure


def as_decimal(value) -> Decimal:
    return Decimal(str(value))

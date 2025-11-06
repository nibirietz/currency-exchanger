from dataclasses import dataclass


@dataclass
class CurrencyPost:
    name: str
    code: str
    sign: str

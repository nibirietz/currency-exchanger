from dataclasses import dataclass


@dataclass
class CurrencyDto:
    id: int
    name: str
    code: str
    sign: str

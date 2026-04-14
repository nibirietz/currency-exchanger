from dataclasses import dataclass


@dataclass
class Currency:
    name: str
    code: str
    sign: str


@dataclass
class CurrencyRequest(Currency):
    def __post_init__(self):
        self.code = self.code.upper().strip()
        print(self.code)
        if len(self.code) != 3 or not self.code.isascii():
            raise ValueError("Код должен состоять из 3 символов.")
        if not (1 <= len(self.sign) <= 2) or not self.sign.isascii():
            raise ValueError("Знак должен состоять из 1 или 2 символов.")


@dataclass
class CurrencyResponse(Currency):
    id: int

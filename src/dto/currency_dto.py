from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class CurrencyRequest:
    name: str
    code: str
    sign: str

    @classmethod
    def create(cls, name: str, code: str, sign: str) -> Self:
        code = code.strip().upper()
        sign = sign.strip()
        name = name.strip()
        print(f"{sign=}")
        if len(code) != 3:
            raise ValueError("Код должен состоять из 3 символов.")
        if not code.isascii() or not code.isalpha():
            raise ValueError("Код должен состоять только из латинских букв.")
        if not (1 <= len(sign) <= 3):
            raise ValueError("Знак должен состоять из 1-2 символов.")
        if not (1 <= len(name) <= 30):
            raise ValueError("Имя должно состоять из 1-30 символов.")
        return cls(name=name, code=code, sign=sign)


@dataclass(frozen=True, slots=True)
class CurrencyResponse:
    id: int
    name: str
    code: str
    sign: str

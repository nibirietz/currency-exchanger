from dataclasses import dataclass


@dataclass
class CurrencyPost:
    name: str
    code: str
    sign: str

    def __post_init__(self):
        self.code = self.code.upper().strip()
        print(self.code)
        if len(self.code) != 3 or not self.code.isascii():
            raise ValueError("Код должен быть длины 3.")

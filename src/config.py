from pathlib import Path
from typing import final


@final
class Config:
    DATABASE_PATH = Path("src/database/db.sqlite")

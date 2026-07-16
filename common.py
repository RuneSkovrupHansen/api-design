from typing import Final
from pydantic import BaseModel

DB_PATH: Final[str] = "app.db"

class Pokemon(BaseModel):
    id: int
    name: str
    types: list[int]

class PokemonType(BaseModel):
    id: int
    name: str
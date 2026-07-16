"""Database models and engine configuration.

Defines the SQLModel ORM models for Pokemon, their types, and the
many-to-many link table between them, along with the SQLite engine
used to connect to the database.
"""

from sqlmodel import Field, Relationship, SQLModel, create_engine

from common import DB_PATH


class PokemonTypeLink(SQLModel, table=True):
    __tablename__ = "pokemon_types"

    pokemon_id: int | None = Field(
        default=None, foreign_key="pokemon.id", primary_key=True
    )
    type_id: int | None = Field(
        default=None, foreign_key="pokemon_type.id", primary_key=True
    )


class PokemonType(SQLModel, table=True):
    __tablename__ = "pokemon_type"

    id: int | None = Field(default=None, primary_key=True)
    name: str


class Pokemon(SQLModel, table=True):
    __tablename__ = "pokemon"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    types: list[PokemonType] = Relationship(link_model=PokemonTypeLink)


engine = create_engine(f"sqlite:///{DB_PATH}")

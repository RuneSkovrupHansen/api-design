"""Populate the local Pokemon database from the PokeAPI.

Fetches Pokemon and their types asynchronously from the public PokeAPI,
validates the responses into the local models, and writes them into the
SQLite database used by the application.
"""

from typing import Final
import sqlite3
import asyncio

from pydantic import field_validator

from common import Pokemon, PokemonType, DB_PATH
import aiohttp

POKEAPI: Final[str] = "https://pokeapi.co/api/v2/"


# Subclass Pokemon to add validation to retrieve data from PokeAPI
class PokemonCreate(Pokemon):
    @field_validator("types", mode="before")
    @classmethod
    def parse_type_ids(cls, types):
        # each item is {"slot": ..., "type": {"name": ..., "url": ...}}
        return [
            int(t["type"]["url"].rstrip("/").rsplit("/", 1)[-1])
            for t in types
        ]

async def get_pokemon(id: int) -> Pokemon:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{POKEAPI}/pokemon/{id}") as res:
            assert res.status == 200
            return PokemonCreate.model_validate_json(await res.text())

async def get_pokemon_type(id: int) -> PokemonType:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{POKEAPI}/type/{id}") as res:
            assert res.status == 200
            return PokemonType.model_validate_json(await res.text())

async def create_pokemon_db():

    # Get a couple of Pokemon
    number_of_pokemons = 10
    pokemons = await asyncio.gather(*(get_pokemon(i) for i in range(1, number_of_pokemons+1)))
    
    # Get types for the Pokemon
    unique_types = {t for pokemon in pokemons for t in pokemon.types}
    pokemon_types = await asyncio.gather(*(get_pokemon_type(t) for t in unique_types))

    # Create a SQLite database
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS pokemon_type (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS pokemon_types (
                pokemon_id INTEGER NOT NULL,
                type_id INTEGER NOT NULL,
                PRIMARY KEY (pokemon_id, type_id),
                FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
                FOREIGN KEY (type_id) REFERENCES pokemon_type (id)
            )
            """
        )

        con.executemany(
            "INSERT OR REPLACE INTO pokemon (id, name) VALUES (?, ?)",
            [(p.id, p.name) for p in pokemons],
        )
        con.executemany(
            "INSERT OR REPLACE INTO pokemon_type (id, name) VALUES (?, ?)",
            [(t.id, t.name) for t in pokemon_types],
        )
        con.executemany(
            "INSERT OR REPLACE INTO pokemon_types (pokemon_id, type_id) VALUES (?, ?)",
            [(p.id, type_id) for p in pokemons for type_id in p.types],
        )
        con.commit()

async def main():
    await create_pokemon_db()

if __name__ == "__main__":
    asyncio.run(main())

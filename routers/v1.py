from common import Pokemon, PokemonType, DB_PATH
import sqlite3

from fastapi import APIRouter, HTTPException

v1 = APIRouter(prefix="/v1")

@v1.get("/pokemon/{id}")
def get_pokemon(id: int) -> Pokemon:
    with sqlite3.connect(DB_PATH) as con:
        row = con.execute(
            "SELECT id, name FROM pokemon WHERE id = ?",
            (id,),
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Pokemon not found")

        type_ids = [
            type_id
            for (type_id,) in con.execute(
                "SELECT type_id FROM pokemon_types WHERE pokemon_id = ?",
                (id,),
            ).fetchall()
        ]

    # Previously, before validation moved into the PokemonCreate
    # subclass, we had to use `model_construct()` to avoid the
    # validation set up for PokeAPI.
    return Pokemon(id=row[0], name=row[1], types=type_ids)

@v1.get("/types/{id}")
def get_types(id: int) -> PokemonType:
    with sqlite3.connect(DB_PATH) as con:
        row = con.execute(
            "SELECT id, name FROM pokemon_type WHERE id = ?",
            (id,),
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Type not found")
        
        return PokemonType(id=row[0], name=row[1])

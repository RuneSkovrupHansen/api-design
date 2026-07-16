from db import Pokemon, PokemonType, engine
from .v1 import get_types

from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, Session


# v2 returns the full type objects rather than just their ids.
class PokemonV2(SQLModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    types: list[PokemonType]

v2 = APIRouter(prefix="/v2")

@v2.get("/pokemon/{id}")
def get_pokemons(id: int) -> PokemonV2:

    # Here we'll use an ORM setup for more ergonomic handling.
    with Session(engine) as session:
        pokemon = session.get(Pokemon, id)

        if pokemon is None:
            raise HTTPException(status_code=404, detail="Pokemon not found")

        return PokemonV2.model_validate(pokemon)

# We're happy with the behavior for get_types so we can just
# reuse v1's handler under the /v2 prefix.
v2.add_api_route("/types/{id}", get_types, methods=["GET"])
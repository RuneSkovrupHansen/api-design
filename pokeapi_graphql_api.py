import asyncio

import aiohttp

POKEAPI_GRAPHQL_URL = "https://graphql.pokeapi.co/v1beta2"

# Note that it is possible to specify multiple root
# query fields to return more data.
QUERY = """
{
  pokemon(limit: 3) {
    id
    name
    pokemontypes {
      type {
        name
      }
    }
  }
}
"""

"""
Example response:
{
  "data": {
    "pokemon": [
      {
        "id": 1,
        "name": "bulbasaur",
        "pokemontypes": [
          {"type": {"name": "grass"}},
          {"type": {"name": "poison"}}
        ]
      },
      {
        "id": 2,
        "name": "ivysaur",
        "pokemontypes": [
          {"type": {"name": "grass"}},
          {"type": {"name": "poison"}}
        ]
      },
      {
        "id": 3,
        "name": "venusaur",
        "pokemontypes": [
          {"type": {"name": "grass"}},
          {"type": {"name": "poison"}}
        ]
      }
    ]
  }
}
"""

async def fetch_pokemon() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            POKEAPI_GRAPHQL_URL, json={"query": QUERY}
        ) as response:
            response.raise_for_status()
            return await response.json()


async def main() -> None:
    result = await fetch_pokemon()
    print(result)
    for pokemon in result["data"]["pokemon"]:
        print(pokemon)


if __name__ == "__main__":
    asyncio.run(main())

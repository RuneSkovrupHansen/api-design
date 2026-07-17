# api-design

Repository for experimenting with API design.

## Initialize the database

Before running the API, populate the local SQLite database. This fetches a handful of Pokemon and their types from the PokeAPI and writes them to disk:

```bash
uv run create_pokemon_db.py
```

## REST

`rest_api.py` defines a FastAPI app that mounts two versioned routers (`/v1` and `/v2`), each exposing `/pokemon/{id}` and `/types/{id}` endpoints.

The versions expose the same data with different shapes: v1 returns a Pokemon's types as a list of type ids, while v2 returns the full type objects.

Run the FastAPI:

```bash
uv run fastapi dev rest_api.py
```

Fetch the same Pokemon from each version:

```bash
# v1 returns types as ids
curl http://127.0.0.1:8000/v1/pokemon/1
# {"id":1,"name":"bulbasaur","types":[12,4]}

# v2 returns the full type objects
curl http://127.0.0.1:8000/v2/pokemon/1
# {"id":1,"name":"bulbasaur","types":[{"id":12,"name":"grass"},{"id":4,"name":"poison"}]}
```

## GraphQL

Run GraphQL API:

```bash
uv run strawberry dev graphql_api
```

Because Strawberry takes a code-first approach, the schema is defined in Python. To export it as SDL, run:

```bash
uv run strawberry export-schema graphql_api > schema.graphql
```


from typing import Final

import strawberry

@strawberry.type
class Zone:
    name: str
    level: int

@strawberry.type
class Continent:
    name: str
    zones: list[Zone]

KALIMDOOR_ZONES: Final[list[Zone]] = [
    Zone(name="Durotar", level=1),
    Zone(name="Mulgore", level=1),
    Zone(name="Teldrassil", level=1),
    Zone(name="Darkshore", level=10),
    Zone(name="The Barrens", level=10),
    Zone(name="Stonetalon Mountains", level=15),
    Zone(name="Ashenvale", level=18),
    Zone(name="Thousand Needles", level=25),
    Zone(name="Desolace", level=30),
    Zone(name="Dustwallow Marsh", level=35),
    Zone(name="Feralas", level=40),
    Zone(name="Tanaris", level=40),
    Zone(name="Azshara", level=45),
    Zone(name="Felwood", level=48),
    Zone(name="Un'Goro Crater", level=48),
    Zone(name="Silithus", level=55),
    Zone(name="Winterspring", level=55),
]

EASTERN_KINGDOMS_ZONES: Final[list[Zone]] = [
    Zone(name="Elwynn Forest", level=1),
    Zone(name="Dun Morogh", level=1),
    Zone(name="Tirisfal Glades", level=1),
    Zone(name="Loch Modan", level=10),
    Zone(name="Silverpine Forest", level=10),
    Zone(name="Westfall", level=10),
    Zone(name="Redridge Mountains", level=15),
    Zone(name="Duskwood", level=18),
    Zone(name="Hillsbrad Foothills", level=20),
    Zone(name="Wetlands", level=20),
    Zone(name="Arathi Highlands", level=30),
    Zone(name="Stranglethorn Vale", level=30),
    Zone(name="Badlands", level=35),
    Zone(name="Swamp of Sorrows", level=35),
    Zone(name="The Hinterlands", level=40),
    Zone(name="Searing Gorge", level=43),
    Zone(name="Blasted Lands", level=45),
    Zone(name="Burning Steppes", level=50),
    Zone(name="Western Plaguelands", level=51),
    Zone(name="Eastern Plaguelands", level=53),
    Zone(name="Deadwind Pass", level=55),
]

# Declare root level queries

@strawberry.type
class Query:

    # We still need to specify and implement the possible queries,
    # the root fields and their resolvers, but field selection is free
    @strawberry.field
    def continents(self) -> list[Continent]:
        return [
            Continent(
                name="Kalimdor",
                zones=KALIMDOOR_ZONES
            ),
            Continent(
                name="Eastern Kingdoms",
                zones=EASTERN_KINGDOMS_ZONES
            ),
        ]
    
    # Optional arg -> nullable GraphQL argument, defaults to null
    @strawberry.field
    def zones(self, min_level: int | None = None) -> list[Zone]:
        all_zones = KALIMDOOR_ZONES + EASTERN_KINGDOMS_ZONES
        return [zone for zone in all_zones if min_level is None or zone.level >= min_level]


schema = strawberry.Schema(query=Query)
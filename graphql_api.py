from typing import Final

import strawberry

@strawberry.type
class Dungeon:
    name: str

@strawberry.type
class Zone:
    name: str
    level: int
    # The strawberry.field(default_factory=...) is required for mutable defaults, lists, dicts
    dungeons: list[Dungeon] = strawberry.field(default_factory=list)

@strawberry.input
class ZoneFilter:
    """Filter for zone queries.

    Example:
        {
          zones(filter: { minLevel: 30, hasDungon: true }) {
            name
            level
            dungeons { name }
          }
        }
    """

    min_level: int | None = None
    has_dungon: bool | None = None

@strawberry.input
class Pagination:
    offset: int = 0
    # Consider clamping limit to protect server
    limit: int = 0

@strawberry.type
class Continent:
    name: str
    zones: list[Zone]

KALIMDOOR_ZONES: Final[list[Zone]] = [
    Zone(name="Durotar", level=1, dungeons=[Dungeon(name="Ragefire Chasm")]),
    Zone(name="Mulgore", level=1),
    Zone(name="Teldrassil", level=1),
    Zone(name="Darkshore", level=10),
    Zone(
        name="The Barrens",
        level=10,
        dungeons=[
            Dungeon(name="Wailing Caverns"),
            Dungeon(name="Razorfen Kraul"),
        ],
    ),
    Zone(name="Stonetalon Mountains", level=15),
    Zone(name="Ashenvale", level=18, dungeons=[Dungeon(name="Blackfathom Deeps")]),
    Zone(name="Thousand Needles", level=25, dungeons=[Dungeon(name="Razorfen Downs")]),
    Zone(name="Desolace", level=30, dungeons=[Dungeon(name="Maraudon")]),
    Zone(name="Dustwallow Marsh", level=35),
    Zone(name="Feralas", level=40, dungeons=[Dungeon(name="Dire Maul")]),
    Zone(name="Tanaris", level=40, dungeons=[Dungeon(name="Zul'Farrak")]),
    Zone(name="Azshara", level=45),
    Zone(name="Felwood", level=48),
    Zone(name="Un'Goro Crater", level=48),
    Zone(name="Silithus", level=55),
    Zone(name="Winterspring", level=55),
]

EASTERN_KINGDOMS_ZONES: Final[list[Zone]] = [
    Zone(name="Elwynn Forest", level=1, dungeons=[Dungeon(name="The Stockade")]),
    Zone(name="Dun Morogh", level=1, dungeons=[Dungeon(name="Gnomeregan")]),
    Zone(name="Tirisfal Glades", level=1, dungeons=[Dungeon(name="Scarlet Monastery")]),
    Zone(name="Loch Modan", level=10),
    Zone(name="Silverpine Forest", level=10, dungeons=[Dungeon(name="Shadowfang Keep")]),
    Zone(name="Westfall", level=10, dungeons=[Dungeon(name="The Deadmines")]),
    Zone(name="Redridge Mountains", level=15),
    Zone(name="Duskwood", level=18),
    Zone(name="Hillsbrad Foothills", level=20),
    Zone(name="Wetlands", level=20),
    Zone(name="Arathi Highlands", level=30),
    Zone(name="Stranglethorn Vale", level=30),
    Zone(name="Badlands", level=35, dungeons=[Dungeon(name="Uldaman")]),
    Zone(
        name="Swamp of Sorrows",
        level=35,
        dungeons=[Dungeon(name="The Temple of Atal'Hakkar")],
    ),
    Zone(name="The Hinterlands", level=40),
    Zone(name="Searing Gorge", level=43, dungeons=[Dungeon(name="Blackrock Depths")]),
    Zone(name="Blasted Lands", level=45),
    Zone(
        name="Burning Steppes",
        level=50,
        dungeons=[Dungeon(name="Lower Blackrock Spire")],
    ),
    Zone(name="Western Plaguelands", level=51, dungeons=[Dungeon(name="Scholomance")]),
    Zone(name="Eastern Plaguelands", level=53, dungeons=[Dungeon(name="Stratholme")]),
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
    def zones(self, filter: ZoneFilter | None = None, pagination: Pagination | None = None) -> list[Zone]:
        zones = KALIMDOOR_ZONES + EASTERN_KINGDOMS_ZONES

        if filter:
            if filter.min_level:
                zones = [zone for zone in zones if zone.level >= filter.min_level]
            
            if filter.has_dungon is True:
                zones = [zone for zone in zones if zone.dungeons]
            elif filter.has_dungon is False:
                zones = [zone for zone in zones if not zone.dungeons]

        if pagination:
            if pagination.offset + pagination.limit > len(zones):
                return []

            zones = zones[pagination.offset : pagination.offset + pagination.limit]

        return zones

schema = strawberry.Schema(query=Query)
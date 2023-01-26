from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class Faction:
    name: str
    color: str  # TODO replace with a more appropriate type


@dataclass
class Territory:
    name: str
    owner: Optional[Faction]


@dataclass
class Map:
    default_territory = Territory("Plains", None)

    territories: List[Territory]
    width: int
    height: int


@dataclass
class Player:
    name: str = "N/A"
    color: str = ""
    faction: Optional[Faction] = None

    def __init__(self, name="N/A", color="", faction=None):
        self.name = name
        self.color = color
        self.faction = faction
        self.assets = {
            "Territories": [],
            "Gold": 1000,
            "Armies": []
        }


@dataclass
class GameWorld:
    factions: List[Faction]
    players: List[Player]
    map: Map

    def combat_simulator(self, army_list):
        pass

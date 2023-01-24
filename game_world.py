from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Faction:
    name: str
    color: str  # TODO replace with a more appropriate type

@dataclass
class Territory:
    name: str
    owner: Faction

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
    factions: list[Faction]
    players: list[Player]
    territories: list[Territory]

    def combat_simulator(self, army_list):
        pass

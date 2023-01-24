from dataclasses import dataclass
from game_world import Territory, Faction, Player
import random
from logging import debug
import logging

logging.basicConfig(level=logging.DEBUG)

@dataclass
class Lobby:
    players: list[Player] = ()
    territories: list[Territory] = ()
    factions: set[Faction] = ()
    expected_num_players: int = 0

    def __init__(self, players, territories, landless_factions):
        self.players = players
        self.territories = territories
        self.factions = set(landless_factions + [territory.owner for territory in territories])

    @property
    def open_factions(self):
        taken_factions = set(player.faction for player in self.players)
        return list(self.factions - taken_factions)

    def join(self, player):
        self.players.append(player)

    def setup_menu(self):
        while not (0 < self.expected_num_players <= 4):
            try:
                user_input = input("Enter number of players (1-4): ")
                debug(f"[{user_input}] => {int(user_input)}")
                self.expected_num_players = int(user_input)
            except ValueError:  # parsing failed
                debug(f"parsing failed, got {user_input}")

    def wait_for_players(self):
        while self.expected_num_players > len(self.players):
            name = input(f"Enter player {len(self.players)+1} name: ")
            faction = random.choice(self.open_factions)
            print(f"{name} is: {faction}")
            new_player = Player(name=name, faction=faction)
            self.join(new_player)
    def start_game(self):
        pass

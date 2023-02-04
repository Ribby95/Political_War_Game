import asyncio
from dataclasses import dataclass
from enum import Enum
from sys import stdout
from typing import List, Union, Tuple, Dict
import aioconsole

import netcode.server
from netcode import messages
from netcode.client import Client
from netcode.messages import Message
from user_interface import test_interface
import user_interface.test_interface


class TileValue(Enum):
    X = 'X'
    O = 'O'

    def __str__(self):
        return self.value


Move = Tuple[TileValue, int]


class TicTacToeGame:
    gameboard: List[Union[TileValue, None]]
    width: int = 3
    height: int = 3

    def __init__(self):
        self.gameboard = [None] * (self.width * self.height)

    def __getitem__(self, item):
        return self.gameboard[item]

    def rows(self):
        for row_num in range(self.height):
            yield self[(row_num * self.width):((row_num + 1) * self.width)]

    def legal_moves(self, player_tile: TileValue):
        return {(player_tile, i) for (i, v) in enumerate(self.gameboard) if v is None}

    def play_move(self, move: Move):
        (tile, index) = move
        if move in self.legal_moves(tile):
            self.gameboard[index] = tile
        else:
            raise ValueError("illegal move")

    def winner(self) -> Union[TileValue, None]:
        complete_rows = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        }
        complete_cols = {
            {1, 4, 7},
            {2, 5, 8},
            {3, 6, 9}
        }
        diagonals = {
            {1, 5, 9},
            {3, 5, 7}
        }
        winning_states = set.union(complete_rows, complete_cols, diagonals)
        xs = {i for (i, v) in enumerate(self.gameboard) if v == TileValue.X}
        os = {i for (i, v) in enumerate(self.gameboard) if v == TileValue.O}
        for win_condition in winning_states:
            if win_condition.issubset(xs):
                return TileValue.X
            elif win_condition.issubset(os):
                return TileValue.O
        return None  # no one won

    def done(self):
        return not any(tile is None for tile in self.gameboard)


@dataclass
class MoveMessage(messages.Message):
    move: int
    tile: TileValue

    def to_move(self):
        return self.tile, self.move

@dataclass
class TextInterface:
    game_state: TicTacToeGame
    tile: TileValue = None
    horizontal_separator = '|'
    vertical_separator = '\n-+-+-\n'

    def handle_input(self, input: str):
        match input.strip().split():
            case ["/move", x]:
                move = int(x)
                return MoveMessage(move=move, tile=self.tile, sender_id=None)
            case _:
                return messages.Chat(sender_id = None, text = input)

    def display(self, output=stdout):
        representation = self.vertical_separator.join(
            self.horizontal_separator.join(
                (
                    str(x.value if x is not None else i + j * 3) for (i, x) in enumerate(row)
                )
            ) for (j, row) in enumerate(self.game_state.rows())
        )

        print(representation, file=output)


@dataclass
class ChooseTile(messages.Message):
    tile: TileValue = TileValue.X


def only(x):
    (val,) = x
    return val


class MessageHandler(test_interface.MessageHandler):
    interface: TextInterface
    id: int = None

    def __init__(self, interface, output=stdout):
        super().__init__(output)
        self.usernames = dict()
        self.interface=interface

    @user_interface.test_interface.MessageHandler.handle.register
    def handleID(self, message: messages.YouAre):
        if message.sender_id == netcode.server.Server.SENDER_ID:
            self.id = message.user_id

    @user_interface.test_interface.MessageHandler.handle.register
    def handleTile(self, message: ChooseTile):
        if self.interface.tile is not None:
            if message.sender_id == self.id:
                self.interface.tile = message.tile
            else:
                leftover = only(set(TileValue) - {message.tile})
                self.interface.tile = leftover

    @user_interface.test_interface.MessageHandler.handle.register
    def handle_move(self, move: MoveMessage):
        self.interface.game_state.play_move(move.to_move())
        self.interface.display()


async def main():
    client = await Client.connect("localhost", 1337)
    # await client.send(ChooseTile(sender_id=None, tile=TileValue.X))

    username = input("username>")
    await client.send(messages.SetUsername(sender_id=None, username=username))

    game = TicTacToeGame()
    interface = TextInterface(game)
    handler = MessageHandler(interface=interface)

    asyncio.create_task(
        test_interface.client_loop(client, handler)
    )

    interface.display()
    while True:
        command: str = await aioconsole.ainput("")
        try:
            message = interface.handle_input(command)
            await client.send(message)
        except ValueError:
            print(f"{command} is not a valid input")


import logging
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())



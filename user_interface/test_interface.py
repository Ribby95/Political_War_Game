import logging
import asyncio
from argparse import ArgumentParser
from sys import stdout
from functools import singledispatchmethod
from typing import Optional

import aioconsole

from logging import debug, info
from netcode.client import Client
from netcode.server import Server
from netcode import messages


async def client_loop(client, output=stdout):
    debug("started client loop")
    handler = MessageHandler(output)
    while True:
        message = await client.receive()
        handler.handle(message)

usernames=dict()

class MessageHandler:
    def __init__(self, output=stdout):
        self.usernames=usernames  # global
        self.output = output

    @singledispatchmethod
    def handle(self, message):
        raise NotImplementedError(f"unexpected message {message}")

    @handle.register
    def handle_chat(self, message: messages.Chat):
        name = self.usernames.get(message.sender_id, message.sender_id)
        print(name,"> ", message.text, sep='', file=self.output)
        self.output.flush()

    @handle.register
    def handle_username(self, message: messages.SetUsername):
        self.usernames[message.sender_id] = message.username

    @handle.register
    def handle_peer_disconnect(self, message: messages.UserDisconnect):
        dropped = message.user_id
        name = f"User {dropped}"
        if dropped in self.usernames.keys():
            name = self.usernames[dropped]
            del self.usernames[dropped]
        print(f"*{name} disconnected*")


def loopup_id(lookup_name: str, usernames: dict) -> Optional[int]:
    for (id, name) in usernames.items():
        if name == lookup_name:
            return id
    return None

def handle_input(input: str) -> messages.Message:
    match input.strip().split():
        case ["/user", *username]:
            return messages.SetUsername(sender_id=None, username='_'.join(username))
        case ["/kick", user]:  # I'm being sneaky
            dropped = loopup_id(user, usernames)
            if dropped is not None:
                return messages.UserDisconnect(sender_id=Server.SENDER_ID, user_id=dropped)
            else:
                messages.Chat(sender_id=None, text="I'm trying to hack (poorly)")
        case _:  # fallback to just sending input as a message
            return messages.Chat(
                sender_id=None,
                text=input.strip(),
            )

async def main(host, port: int):
    debug("got here")
    client = await Client.connect(host, port)
    asyncio.create_task(client_loop(client, stdout))
    while True:
        command: str = await aioconsole.ainput("")
        message = handle_input(command)
        await client.send(message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument("host", default="localhost")
    parser.add_argument("port", type=int, default=Server.PORT)

    args = parser.parse_args()
    asyncio.run(main(**vars(args)))

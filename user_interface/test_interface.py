import logging
import asyncio
from argparse import ArgumentParser
from sys import stdout
from functools import singledispatchmethod
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


class MessageHandler:
    def __init__(self, output=stdout):
        self.usernames=dict()
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


command_map ={
    "/user": lambda arg: messages.SetUsername(sender_id=None, username=arg)
}

def handle_input(input: str):
    input = input.strip()
    if input.startswith("/"):
        (command, args) = input.split(maxsplit=1)
        if (action := command_map.get(command)) is not None:
            return action(args)
        else:
            return None
    else:
        # fallthrough
        return messages.Chat(
            sender_id=None,
            text=input
        )

async def main(host, port: int):
    debug("got here")
    client = await Client.connect(host, port)
    asyncio.create_task(client_loop(client, stdout))
    while True:
        command: str = await aioconsole.ainput("")
        if (message := handle_input(command)) is not None:
            await client.send(message)
        else:
            print("unrecognised command", command.split(maxsplit=1)[0])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument("host", default="localhost")
    parser.add_argument("port", type=int, default=Server.PORT)

    args = parser.parse_args()
    asyncio.run(main(**vars(args)))

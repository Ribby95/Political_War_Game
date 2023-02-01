import asyncio
import logging
import random
import typing

from logging import info, debug
from dataclasses import dataclass

from netcode.client import Client

@dataclass(frozen=False)
class Session:
    id: int
    client: Client


class Server:
    PACKET_SIZE = 2048
    PORT = 1337

    def __init__(self, host, port=PORT):
        self.host = host
        self.port = port

        ids = list(range(1000))
        random.shuffle(ids)
        self.id_pool = iter(ids)

        self.message_history = []
        self.sessions = []

    def close(self):
        debug("socket closing")

    async def start(self):
        # have to get a strong reference to the task so it's not garbage collected
        server_task = asyncio.start_server(
            client_connected_cb=self.handle_client,
            host=self.host,
            port=self.port
        )

        debug("awaiting server task now")
        await server_task
        while True:
            await asyncio.sleep(10)


    async def handle_client(self, client_reader, client_writer):
        debug("handle client initialized")
        new_session = Session(
            id=next(self.id_pool),  # todo add collision avoidance
            client=Client(writer=client_writer, reader=client_reader)
        )
        self.sessions.append(new_session)  # todo make this not a race-condition waiting to happen
        await self.catch_up(new_session)
        await self.forward_messages(new_session)

    async def catch_up(self, new_session: Session):
        for message in self.message_history:
            await new_session.client.send(message)

    async def forward_messages(self, client_session: Session):
        while True:
            debug(f"receive loop {client_session.id} waiting on message from reader")
            message = await client_session.client.receive()
            reply = f"message from {client_session.id}: " + message
            self.message_history.append(reply)
            debug("broadcasting")
            await asyncio.gather(
                *(session.client.send(reply) for session in self.sessions)
            )
            debug("done broadcasting")


async def main():
    server = Server(host="localhost", port=1337)
    try:
        await server.start()
    finally:
        server.close()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(module)s/%(funcName)s:%(lineno)d: %(message)s"
    )
    asyncio.run(main(), debug=True)

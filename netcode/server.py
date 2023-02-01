import asyncio
import logging
import random
import socket

from logging import info, debug
from queue import Queue
from dataclasses import dataclass
import pickle


@dataclass(frozen=False)
class Session:
    id: int
    message_queue: Queue = Queue()


class Server:
    PACKET_SIZE = 2048
    PORT = 1337

    def __init__(self, host, port=PORT):
        self.host = host
        self.port = port
        self.message_history = []
        self.sessions = []
        self.inbox = Queue()
        self.tasks = set()

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
            id=random.randint(0, 2 ** 64),  # todo add collision avoidance
            message_queue=Queue()
        )
        self.sessions.append(new_session)  # todo make this not a race-condition waiting to happen
        self.tasks.add(
            asyncio.create_task(
                self.get_messages(client_reader, client_id=new_session.id)
            )
        )
        self.tasks.add(
            asyncio.create_task(
                self.send_messages(client_writer, client_queue=new_session.message_queue)
            )
        )

    async def get_messages(self, client_reader, client_id):
        debug("receive loop initialized")
        while True:
            message = await pickle.load(client_reader)
            debug(f"got message {message!r}")
            message.id = client_id  # todo check if a user tries spoofing ids and spank em
            self.inbox.put(message)
            debug("put message in server inbox")
            await asyncio.sleep(0.1)

    @staticmethod
    async def send_messages(client_writer, client_queue):
        debug("send loop initialized")
        while True:
            message = await client_queue.get()
            pickle.dump(message, client_writer)

    async def broadcast(self):
        debug("broadcaster initialized")
        while True:
            message = await self.inbox.get()
            for session in self.sessions:
                session.message_queue.put(message)


async def main():
    debug("main started")
    server = Server(host="localhost", port=1337)
    debug("awaiting server")
    try:
        await server.start()
    finally:
        server.close()
    debug("done")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

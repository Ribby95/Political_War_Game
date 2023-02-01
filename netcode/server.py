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

    async def start(self):
        # set up broadcast loop
        self.tasks.add(asyncio.create_task(self.broadcast()))

        # WARN for some reason the port doesn't open unless I initialize the socket separately
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()

        # have to get a strong reference to the task so it's not garbage collected
        server_task = asyncio.start_server(
            client_connected_cb=self.handle_client,
            sock=sock
        )
        debug(f"listening on {self.host}:{self.port}")
        self.tasks.add(server_task)
        debug("awaiting server task now")
        await server_task

    async def handle_client(self, client_reader, client_writer):
        debug("handle client initialized")
        new_session = Session(
            id=random.randint(0, 2 ** 64),  # todo add collision avoidance
            message_queue=Queue()
        )
        self.sessions.append(new_session)  # todo make this not a race-condition waiting to happen
        async with asyncio.TaskGroup() as user_tasks:
            user_tasks.create_task(
                self.get_messages(client_reader, client_id=new_session.id)
            )
            user_tasks.create_task(
                self.send_messages(client_writer, client_queue=new_session.message_queue)
            )

    async def get_messages(self, client_reader, client_id):
        debug("receive loop initialized")
        while True:
            message = await pickle.load(client_reader)
            debug(f"got message {message!r}")
            message.id = client_id  # todo check if a user tries spoofing ids and spank em
            self.inbox.put(message)
            debug("put message in server inbox")

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
    await server.start()
    debug("done")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

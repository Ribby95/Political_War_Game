import asyncio
import logging
import random
import socket

from logging import info, debug
from queue import Queue
from dataclasses import dataclass

from netcode import messages


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
            id=0,  # todo add collision avoidance
            message_queue=Queue()
        )
        self.sessions.append(new_session)  # todo make this not a race-condition waiting to happen
        asyncio.gather(
            self.get_messages(client_reader, client_id=new_session.id),
            self.send_messages(client_writer, message_queue=new_session.message_queue)
        )


    async def get_messages(self, client_reader, client_id):
        while True:
            debug(f"receive loop {client_id} waiting on message from reader")
            message = await messages.deserialize(client_reader)
            debug("broadcasting")
            for session in self.sessions:
                session.message_queue.put(message)
            debug("done broadcasting")

    async def send_messages(self, client_writer, message_queue):
        debug("started")
        while True:
            debug("waiting on queue")
            try: 
                message = session.message_queue.get(block=False)
                debug("waiting to serialize")
                await messages.serialize(client_writer, message)
            except queue.Empty:
                await asyncio.sleep()
            debug("done")

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

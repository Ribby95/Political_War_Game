import asyncio
from logging import debug
from queue import Queue
import pickle

from netcode import messages


class Client:

    @staticmethod
    async def new(host, port):
        (reader, writer) = await asyncio.open_connection(host, port)
        return Client(reader, writer)

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send(self, message):
        debug(f"sending {message!r}")
        pickle.dump(message, self.writer)
        await self.writer.drain()

    async def receive(self):
        debug("receiveing message")
        message = pickle.load(await self.reader)
        return message

    async def wait_for_messages(self, output: Queue):
        while True:
            debug("waiting on message from server")
            message = await self.receive()
            debug(f"got message {message}")
            output.put(message)


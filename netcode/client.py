from logging import debug
from asyncio import StreamWriter, StreamReader, open_connection


from netcode import messages


class Client:

    @staticmethod
    async def connect(host, port):
        debug("connecting")
        (reader, writer) = await open_connection(host, port)
        debug("connected")
        return Client(reader, writer)

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

    async def send(self, message):
        debug(f"sending {message!r}")
        await messages.serialize(self.writer, message)

    async def receive(self) -> messages.Message:
        debug("receiving message")
        return await messages.deserialize(self.reader)

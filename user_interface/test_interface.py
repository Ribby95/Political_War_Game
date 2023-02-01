import logging
import asyncio
from argparse import  ArgumentParser
from queue import Queue
from sys import stdout

from logging import debug, info
from netcode.client import Client
from netcode.server import Server


async def client_loop(client, output=stdout):
    debug("started client loop")
    async for message in client.wait_for_messages():
        debug("waiting on message")
        print(message, file=output)
        output.flush()


async def main(host, port: int):
    debug("got here")
    client = await Client.connect(host, port)
    client_loop_task = asyncio.create_task(client_loop(client, stdout))

    while True:
        message = input(">")
        info("sending message")
        await client.send(message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument("host", default="localhost")
    parser.add_argument("port", type=int, default=Server.PORT)

    args = parser.parse_args()
    asyncio.run(main(**vars(args)))

import logging
import asyncio
from argparse import  ArgumentParser
from sys import stdout
import aioconsole

from logging import debug, info
from netcode.client import Client
from netcode.server import Server


async def client_loop(client, output=stdout):
    debug("started client loop")
    while True:
        message = await client.receive()
        print(message, file=output)
        debug("flushing output")
        output.flush()


async def main(host, port: int):
    debug("got here")
    client = await Client.connect(host, port)
    asyncio.create_task(client_loop(client, stdout))
    while True:
        message = await aioconsole.ainput(">")
        info(f"sending message {message!r}")
        await client.send(message.encode())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument("host", default="localhost")
    parser.add_argument("port", type=int, default=Server.PORT)

    args = parser.parse_args()
    asyncio.run(main(**vars(args)))

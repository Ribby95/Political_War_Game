import logging
import asyncio
from argparse import  ArgumentParser
from queue import Queue
from sys import stdout

from logging import debug, info
from netcode.client import Client
from netcode.server import Server


async def receive_worker(input: Queue, outfile):
    while True:
        debug("waiting on message")
        print(input.get(block=True),file=outfile)
        debug("got message")


async def send_input(client):
    message = input(">")
    info("sending message")
    client.send(message)


async def main(host, port: int):
    debug("got here")
    inbox = Queue()
    client = await Client.new(host, port)

    task1 = asyncio.create_task(client.wait_for_messages(inbox))  # todo better names
    task2 = asyncio.create_task(receive_worker(inbox, stdout))
    task3 = asyncio.create_task(send_input(client))
    await task3
    await task2
    await task1


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument("host", default="localhost")
    parser.add_argument("port", type=int, default=Server.PORT)

    args = parser.parse_args()
    asyncio.run(main(**vars(args)))

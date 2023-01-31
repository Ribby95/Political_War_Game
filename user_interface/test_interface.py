from netcode.client import Client
from argparse import  ArgumentParser
from queue import Queue
from threading import Thread

def main(host, port: int):
    username = input("username> ")
    client = Client(host, port, username)
    client.join()
    message_queue = Queue()
    server_loop = Thread(target=client.loop, args=(message_queue,))
    server_loop.start()
    while True:
        message = message_queue.get()
        print(message)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port", type=int)

    args = parser.parse_args()
    main(**vars(args))

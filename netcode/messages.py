from logging import debug

async def deserialize(reader):
    debug("reading")
    message = await reader.reader.readline()
    debug(f"read message {message!r}")
    return message.decode()

async def serialize(writer, message):
    message += '\n\n\n'
    message = message.encode()
    debug(f"writing {message!r}")
    writer.write(message)
    debug("draining")
    await writer.drain()
    debug("write complete")


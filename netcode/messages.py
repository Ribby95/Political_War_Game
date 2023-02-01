from logging import debug
import struct
async def deserialize(reader):
    debug("reading")
    size, = struct.unpack('<L', await reader.readexactly(4))
    debug(f"got message of size {size}")
    message = await reader.readexactly(size)
    debug(f"got message {message!r}")
    return message


async def serialize(writer, message):
    message = message.encode()
    debug(f"writing {message!r} len {len(message)}")
    writer.write(struct.pack('<L', len(message)))
    writer.write(message)
    await writer.drain()
    debug("write done")


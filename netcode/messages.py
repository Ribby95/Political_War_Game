from logging import debug
import struct
import pickle

async def deserialize(reader):
    debug("reading")
    size, = struct.unpack('<L', await reader.readexactly(4))
    debug(f"got message of size {size}")
    data = await reader.readexactly(size)
    message = pickle.loads(data)
    debug(f"got message {message!r}")
    return message


async def serialize(writer, message):
    data = pickle.dumps(message)
    debug(f"writing {data!r} len {len(data)}")
    writer.write(struct.pack('<L', len(data)))
    writer.write(data)
    await writer.drain()
    debug("write done")


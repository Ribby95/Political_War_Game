import pickle

async def deserialize(reader):
    return pickle.load(await reader)

async def serialize(writer, message):
    pickle.dump(writer, message)
    await writer.drain()


#AxiomForceSub --by OwnerAxiom
from .mongo import channels


async def add_channel(chat_id: int):
    if not await channels.find_one({"_id": chat_id}):
        await channels.insert_one({"_id": chat_id})


async def get_channels():
    async for chat in channels.find():
        yield chat["_id"]


async def total_channels():
    return await channels.count_documents({})

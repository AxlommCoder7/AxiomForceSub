#AxiomForceSub --by OwnerAxiom
from .mongo import CHANNELS


async def add_channel(chat_id: int):

    await CHANNELS.update_one(
        {"_id": chat_id},
        {
            "$setOnInsert": {
                "_id": chat_id
            }
        },
        upsert=True,
    )


async def delete_channel(chat_id: int):

    await CHANNELS.delete_one(
        {"_id": chat_id}
    )


async def get_channels():

    async for chat in CHANNELS.find():

        yield chat["_id"]


async def total_channels():

    return await CHANNELS.count_documents({})

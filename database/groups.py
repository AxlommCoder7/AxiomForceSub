#AxiomForceSub --by OwnerAxiom
from .mongo import GROUPS


async def add_group(chat_id: int):

    await GROUPS.update_one(
        {"_id": chat_id},
        {
            "$setOnInsert": {
                "_id": chat_id
            }
        },
        upsert=True,
    )


async def delete_group(chat_id: int):

    await GROUPS.delete_one(
        {"_id": chat_id}
    )


async def get_groups():

    async for chat in GROUPS.find():

        yield chat["_id"]


async def total_groups():

    return await GROUPS.count_documents({})

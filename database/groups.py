#AxiomForceSub --by OwnerAxiom
from .mongo import groups


async def add_group(chat_id: int):
    if not await groups.find_one({"_id": chat_id}):
        await groups.insert_one({"_id": chat_id})


async def get_groups():
    async for chat in groups.find():
        yield chat["_id"]


async def total_groups():
    return await groups.count_documents({})

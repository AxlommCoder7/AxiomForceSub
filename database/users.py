#AxiomForceSub --by OwnerAxiom
from .mongo import users


async def add_user(user_id: int):
    if not await users.find_one({"_id": user_id}):
        await users.insert_one({"_id": user_id})


async def is_user(user_id: int):
    return await users.find_one({"_id": user_id})


async def get_users():
    async for user in users.find():
        yield user["_id"]


async def total_users():
    return await users.count_documents({})

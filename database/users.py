#AxiomForceSub --by OwnerAxiom
from .mongo import USERS


async def add_user(user_id: int):

    await USERS.update_one(
        {"_id": user_id},
        {
            "$setOnInsert": {
                "_id": user_id
            }
        },
        upsert=True,
    )


async def delete_user(user_id: int):

    await USERS.delete_one(
        {"_id": user_id}
    )


async def is_user(user_id: int):

    return await USERS.find_one(
        {"_id": user_id}
    )


async def get_users():

    async for user in USERS.find():

        yield user["_id"]


async def total_users():

    return await USERS.count_documents({})

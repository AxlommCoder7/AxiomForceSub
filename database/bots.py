from .mongo import BOTS


async def add_bot(owner_id: int, token: str):

    await BOTS.update_one(
        {
            "_id": owner_id
        },
        {
            "$set": {
                "token": token
            }
        },
        upsert=True,
    )


async def remove_bot(owner_id: int):

    await BOTS.delete_one(
        {
            "_id": owner_id
        }
    )


async def get_bot(owner_id: int):

    return await BOTS.find_one(
        {
            "_id": owner_id
        }
    )


async def get_all_bots():

    async for bot in BOTS.find():

        yield bot

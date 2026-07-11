#AxiomForceSub --by OwnerAxiom
from .mongo import SETTINGS


async def set_force_sub(owner_id: int, chat_id: int):

    await SETTINGS.update_one(
        {
            "_id": owner_id
        },
        {
            "$set": {
                "force_sub": chat_id
            }
        },
        upsert=True,
    )


async def get_force_sub(owner_id: int):

    data = await SETTINGS.find_one(
        {
            "_id": owner_id
        }
    )

    if data:

        return data.get("force_sub")

    return None


async def remove_force_sub(owner_id: int):

    await SETTINGS.update_one(
        {
            "_id": owner_id
        },
        {
            "$unset": {
                "force_sub": ""
            }
        }
    )

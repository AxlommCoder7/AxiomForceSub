#AxiomForceSub --by OwnerAxiom
from .mongo import settings


async def set_force_sub(chat_id):
    await settings.update_one(
        {"_id": "forcesub"},
        {"$set": {"chat_id": chat_id}},
        upsert=True,
    )


async def get_force_sub():
    data = await settings.find_one({"_id": "forcesub"})
    if data:
        return data["chat_id"]
    return None

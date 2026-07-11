#AxiomForceSub --by OwnerAxiom
from pyrogram import filters
from config import OWNER_ID


async def _owner(_, __, message):

    if not message.from_user:
        return False

    return message.from_user.id == OWNER_ID


owner_filter = filters.create(_owner)

#AxiomForceSub --by OwnerAxiom
from pyrogram import filters
from config import OWNER_ID


def owner_filter(_, __, message):
    return message.from_user and message.from_user.id == OWNER_ID


owner_filter = filters.create(owner_filter)

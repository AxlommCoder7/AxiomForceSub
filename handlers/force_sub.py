#AxiomForceSub --by OwnerAxiom
from pyrogram import Client
from pyrogram import filters

from config import OWNER_ID
from database.settings import (
    set_force_sub,
    get_force_sub,
    remove_force_sub
)


@Client.on_message(filters.private & filters.command("setfsub"))
async def setfsub(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) != 2:
        return await message.reply_text(
            "/setfsub -100xxxxxxxxxx"
        )

    chat = int(message.command[1])

    await set_force_sub(chat)

    await message.reply_text(
        f"✅ Force Subscribe Set\n\n{chat}"
    )


@Client.on_message(filters.private & filters.command("removefsub"))
async def removefsub(client, message):

    if message.from_user.id != OWNER_ID:
        return

    await remove_force_sub()

    await message.reply_text(
        "✅ Force Subscribe Removed."
    )


@Client.on_message(filters.private & filters.command("fsub"))
async def fsub(client, message):

    if message.from_user.id != OWNER_ID:
        return

    chat = await get_force_sub()

    if chat:
        await message.reply_text(
            f"Current Force Subscribe\n\n{chat}"
        )
    else:
        await message.reply_text(
            "No Force Subscribe Set."
        )

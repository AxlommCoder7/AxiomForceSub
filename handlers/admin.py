#AxiomForceSub --by OwnerAxiom
import os
import signal
import asyncio
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID


OWNER_TEXT = """
👑 **Owner Panel**

Available Commands

/stats
/logs
/gitpull
/restart
/setfsub
/removefsub
/fsub
/broadcast
"""


@Client.on_message(filters.private & filters.command("admin"))
async def admin_panel(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    await message.reply_text(OWNER_TEXT)


@Client.on_message(filters.private & filters.command("restart"))
async def restart_bot(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    msg = await message.reply_text(
        "♻ Restarting..."
    )

    await asyncio.sleep(2)

    await msg.edit_text(
        "✅ Restarted."
    )

    os.kill(os.getpid(), signal.SIGINT)

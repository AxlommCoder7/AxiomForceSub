#AxiomForceSub --by OwnerAxiom
import os

from pyrogram import Client, filters

from config import OWNER_ID


@Client.on_message(filters.private & filters.command("logs"))
async def logs_handler(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if not os.path.exists("logs/bot.log"):

        return await message.reply_text(
            "❌ Log file not found."
        )

    if os.path.getsize("logs/bot.log") == 0:

        return await message.reply_text(
            "⚠ Log file is empty."
        )

    await message.reply_document(
        "logs/bot.log",
        caption="📄 Latest Bot Log"
    )

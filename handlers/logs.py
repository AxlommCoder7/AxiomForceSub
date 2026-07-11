#AxiomForceSub --by OwnerAxiom
import os

from pyrogram import Client, filters

from config import OWNER_ID


@Client.on_message(filters.private & filters.command("logs"))
async def send_logs(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if not os.path.exists("logs/bot.log"):

        return await message.reply_text(
            "No Logs Found."
        )

    await message.reply_document(
        "logs/bot.log",
        caption="📄 Latest Bot Logs"
    )

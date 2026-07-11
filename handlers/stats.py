#AxiomForceSub --by OwnerAxiom
from pyrogram import Client
from pyrogram import filters

from config import OWNER_ID
from database.stats import get_stats


@Client.on_message(filters.private & filters.command("stats"))
async def stats(client, message):

    if message.from_user.id != OWNER_ID:
        return

    data = await get_stats()

    await message.reply_text(
        f"""
📊 **Statistics**

👤 Users : {data['users']}

👥 Groups : {data['groups']}

📢 Channels : {data['channels']}
"""
    )

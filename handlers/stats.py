from datetime import datetime

from pyrogram import Client, filters

from config import OWNER_ID
from database.stats import get_stats
from loader import app
from utils.system import (
    uptime,
    ram,
    cpu,
    system
)


@Client.on_message(
    filters.private &
    filters.command("stats")
)
async def stats_handler(client, message):

    if message.from_user.id != OWNER_ID:
        return

    me = await app.get_me()

    data = await get_stats()

    text = f"""
📊 <b>Axiom ForceSub Statistics</b>

━━━━━━━━━━━━━━━━

🤖 <b>Bot :</b> {me.first_name}

🆔 <b>ID :</b>
<code>{me.id}</code>

👤 <b>Total Users :</b>
<code>{data['users']}</code>

👥 <b>Total Groups :</b>
<code>{data['groups']}</code>

📢 <b>Total Channels :</b>
<code>{data['channels']}</code>

━━━━━━━━━━━━━━━━

💻 <b>System :</b> {system()}

⚙ <b>CPU :</b> {cpu()} %

🧠 <b>RAM :</b> {ram()} %

⏳ <b>Uptime :</b>
<code>{uptime()}</code>

━━━━━━━━━━━━━━━━

🕒 <b>Time :</b>

<code>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</code>
"""

    await message.reply_text(
        text,
        disable_web_page_preview=True
    )

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters.forcesub import force_sub_filter
from database.users import add_user
from database.groups import add_group
from database.channels import add_channel
from utils.logger import LOGGER


START_TEXT = """
👋 **Welcome {}**

I'm a powerful Telegram Management Bot.

✨ Features:

• Force Subscribe
• Broadcast
• Statistics
• Logs
• Git Pull
• More Coming Soon
"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ Add Me",
                url="https://t.me/YourBot?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                "Support",
                url="https://t.me/YourSupport"
            ),
            InlineKeyboardButton(
                "Updates",
                url="https://t.me/YourChannel"
            )
        ]
    ]
)


@Client.on_message(filters.private & filters.command("start") & force_sub_filter)
async def start_private(client, message):

    await add_user(message.from_user.id)

    LOGGER.info(f"User Started : {message.from_user.id}")

    await message.reply_photo(
        photo="assets/start.jpg",
        caption=START_TEXT.format(message.from_user.mention),
        reply_markup=START_BUTTONS
    )


@Client.on_message(filters.group & filters.command("start"))
async def start_group(client, message):

    await add_group(message.chat.id)

    LOGGER.info(f"Group Registered : {message.chat.id}")

    await message.reply_text(
        "✅ Bot is Active."
    )


@Client.on_message(filters.channel & filters.command("start"))
async def start_channel(client, message):

    await add_channel(message.chat.id)

    LOGGER.info(f"Channel Registered : {message.chat.id}")

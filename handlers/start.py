from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import OWNER_ID
from database.users import add_user
from database.groups import add_group
from database.channels import add_channel
from database.settings import get_force_sub
from utils.logger import send_log


START_TEXT = """
👋 <b>Welcome {}</b>

I'm a powerful Force Subscribe Bot.

<b>Features</b>

• Force Subscribe
• Broadcast
• Statistics
• Logger
• Git Pull
• Multi Group Support

Use the buttons below to get started.
"""


@Client.on_message(filters.private & filters.command("start"))
async def start_private(client, message):

    user = message.from_user

    await add_user(user.id)

    await send_log(
        f"👤 <b>New User</b>\n\n"
        f"Name : {user.mention}\n"
        f"ID : <code>{user.id}</code>"
    )

    force = await get_force_sub(OWNER_ID)

    buttons = []

    if force:

        try:

            chat = await client.get_chat(force)

            if chat.username:

                buttons.append(
                    [
                        InlineKeyboardButton(
                            "📢 Join Channel",
                            url=f"https://t.me/{chat.username}"
                        )
                    ]
                )

        except:
            pass

    buttons.append(
        [
            InlineKeyboardButton(
                "➕ Add Me",
                url=f"https://t.me/{(await client.get_me()).username}?startgroup=true"
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                "ℹ Help",
                callback_data="help"
            ),
            InlineKeyboardButton(
                "📊 Stats",
                callback_data="stats"
            )
        ]
    )

    await message.reply_text(
        START_TEXT.format(user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_message(
    filters.group
    & filters.incoming
)
async def register_group(client, message):

    await add_group(message.chat.id)


@Client.on_message(
    filters.channel
    & filters.incoming
)
async def register_channel(client, message):

    await add_channel(message.chat.id)

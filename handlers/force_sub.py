from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    UsernameNotOccupied,
    PeerIdInvalid,
    UserNotParticipant
)

from config import OWNER_ID
from database.settings import (
    set_force_sub,
    get_force_sub,
    remove_force_sub
)
from utils.logger import send_log


# ------------------------------------------
# Set Force Subscribe
# ------------------------------------------

@Client.on_message(filters.private & filters.command("setfsub"))
async def set_fsub(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) != 2:

        return await message.reply_text(
            "Usage:\n\n"
            "<code>/setfsub -100xxxxxxxxxx</code>\n"
            "or\n"
            "<code>/setfsub @channelusername</code>"
        )

    target = message.command[1]

    try:

        chat = await client.get_chat(target)

    except (PeerIdInvalid, UsernameNotOccupied):

        return await message.reply_text(
            "❌ Invalid Chat ID / Username."
        )

    try:

        me = await client.get_me()

        member = await client.get_chat_member(
            chat.id,
            me.id
        )

        if member.status not in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):

            return await message.reply_text(
                "❌ Make me admin first."
            )

    except Exception:

        return await message.reply_text(
            "❌ I must be inside that channel."
        )

    await set_force_sub(
        OWNER_ID,
        chat.id
    )

    await send_log(
        f"⚙ <b>Force Subscribe Updated</b>\n\n"
        f"Chat : {chat.title}\n"
        f"ID : <code>{chat.id}</code>"
    )

    await message.reply_text(
        f"""
✅ <b>Force Subscribe Enabled</b>

<b>Channel :</b> {chat.title}

<b>ID :</b>

<code>{chat.id}</code>
"""
    )


# ------------------------------------------
# Remove Force Subscribe
# ------------------------------------------

@Client.on_message(filters.private & filters.command("removefsub"))
async def remove_fsub(client, message):

    if message.from_user.id != OWNER_ID:
        return

    force = await get_force_sub(OWNER_ID)

    if not force:

        return await message.reply_text(
            "Force Subscribe Already Disabled."
        )

    await remove_force_sub(
        OWNER_ID
    )

    await send_log(
        "❌ Force Subscribe Removed."
    )

    await message.reply_text(
        "✅ Force Subscribe Disabled."
    )


# ------------------------------------------
# Show Current
# ------------------------------------------

@Client.on_message(filters.private & filters.command("fsub"))
async def current_force_sub(client, message):

    if message.from_user.id != OWNER_ID:
        return

    force = await get_force_sub(
        OWNER_ID
    )

    if not force:

        return await message.reply_text(
            "No Force Subscribe Configured."
        )

    try:

        chat = await client.get_chat(force)

        text = f"""
📢 <b>Current Force Subscribe</b>

<b>Name :</b> {chat.title}

<b>ID :</b>

<code>{chat.id}</code>
"""

    except Exception:

        text = f"""
📢 <b>Current Force Subscribe</b>

<code>{force}</code>
"""

    await message.reply_text(text)


# ------------------------------------------
# Check Command
# ------------------------------------------

@Client.on_message(filters.private & filters.command("checkfsub"))
async def check_fsub(client, message):

    if message.from_user.id != OWNER_ID:
        return

    force = await get_force_sub(
        OWNER_ID
    )

    if not force:

        return await message.reply_text(
            "No Force Subscribe Set."
        )

    try:

        member = await client.get_chat_member(
            force,
            message.from_user.id
        )

        if member.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):

            return await message.reply_text(
                "✅ You're Joined."
            )

    except UserNotParticipant:

        return await message.reply_text(
            "❌ You're Not Joined."
        )

    except Exception as e:

        return await message.reply_text(
            f"Error\n\n<code>{e}</code>"
        )

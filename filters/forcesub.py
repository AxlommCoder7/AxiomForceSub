#AxiomForceSub --by OwnerAxiom
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database.settings import get_force_sub


async def check_force_sub(_, client, message):

    if not message.from_user:
        return True

    if message.from_user.is_bot:
        return True

    if not message.chat:
        return True

    if message.chat.type.name != "PRIVATE":
        return True

    owner_id = message.from_user.id

    force_chat = await get_force_sub(owner_id)

    if not force_chat:
        return True

    try:

        member = await client.get_chat_member(
            force_chat,
            owner_id
        )

        if member.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ):
            return True

    except Exception:
        pass

    try:
        chat = await client.get_chat(force_chat)

        if chat.username:

            join_button = InlineKeyboardButton(
                "📢 Join Channel",
                url=f"https://t.me/{chat.username}"
            )

        else:

            join_button = InlineKeyboardButton(
                "📢 Open Channel",
                url="https://telegram.org"
            )

    except Exception:

        join_button = InlineKeyboardButton(
            "📢 Join Channel",
            url="https://telegram.org"
        )

    keyboard = InlineKeyboardMarkup(
        [
            [join_button],
            [
                InlineKeyboardButton(
                    "✅ I've Joined",
                    callback_data="checksub"
                )
            ]
        ]
    )

    try:
        await message.delete()
    except:
        pass

    try:

        await client.send_message(
            owner_id,
            (
                "👋 <b>Access Restricted</b>\n\n"
                "To use this bot, you must first join the required channel.\n\n"
                "After joining, press <b>I've Joined</b>."
            ),
            reply_markup=keyboard
        )

    except:
        pass

    return False


force_sub_filter = filters.create(check_force_sub)

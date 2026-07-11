#AxiomForceSub --by OwnerAxiom
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.settings import get_force_sub


async def check_force_sub(_, client, message):
    if not message.from_user:
        return True

    if message.from_user.is_bot:
        return True

    if message.chat.type.name != "PRIVATE":
        return True

    force_chat = await get_force_sub()

    if not force_chat:
        return True

    try:
        member = await client.get_chat_member(
            force_chat,
            message.from_user.id
        )

        if member.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER
        ):
            return True

    except Exception:
        pass

    try:
        await message.delete()
    except:
        pass

    try:
        chat = await client.get_chat(force_chat)

        if chat.username:
            url = f"https://t.me/{chat.username}"
        else:
            url = f"https://t.me/+{str(force_chat).replace('-100','')}"

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📢 Join Channel",
                        url=url
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ I've Joined",
                        callback_data="checksub"
                    )
                ]
            ]
        )

        await message.reply_text(
            "👋 **Welcome!**\n\n"
            "To continue using this bot, you must first join our official channel.\n\n"
            "After joining, click **I've Joined**.",
            reply_markup=buttons
        )

    except:
        pass

    return False


force_sub_filter = filters.create(check_force_sub)

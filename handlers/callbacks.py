from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import CallbackQuery

from config import OWNER_ID
from database.settings import get_force_sub
from utils.logger import send_log


@Client.on_callback_query(filters.regex("^checksub$"))
async def check_subscription(client: Client, query: CallbackQuery):

    force_chat = await get_force_sub(OWNER_ID)

    if not force_chat:

        return await query.answer(
            "Force Subscribe Disabled.",
            show_alert=True
        )

    try:

        member = await client.get_chat_member(
            force_chat,
            query.from_user.id
        )

        if member.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER
        ):

            await query.answer(
                "Subscription Verified ✅",
                show_alert=True
            )

            await send_log(
                f"✅ User Verified\n\n"
                f"User : {query.from_user.mention}\n"
                f"ID : <code>{query.from_user.id}</code>"
            )

            return await query.message.edit_text(
                f"""
🎉 <b>Verification Successful!</b>

Welcome {query.from_user.mention}

You can now use all commands of this bot.

Send /start to continue.
"""
            )

    except Exception:

        pass

    await query.answer(
        "❌ You haven't joined the required channel yet.",
        show_alert=True
    )


@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(client: Client, query: CallbackQuery):

    await query.answer()

    await query.message.edit_text(
        """
📚 <b>Help Menu</b>

Available Commands

/start - Start Bot

/stats - Statistics (Owner)

/logs - Logs (Owner)

/broadcast - Broadcast (Owner)

/gitpull - Update Bot (Owner)

/setfsub - Set Force Subscribe

/removefsub - Remove Force Subscribe
"""
    )


@Client.on_callback_query(filters.regex("^stats$"))
async def stats_callback(client: Client, query: CallbackQuery):

    if query.from_user.id != OWNER_ID:

        return await query.answer(
            "Owner Only.",
            show_alert=True
        )

    from database.stats import get_stats

    data = await get_stats()

    await query.answer()

    await query.message.edit_text(
        f"""
📊 <b>Bot Statistics</b>

👤 Users : <code>{data['users']}</code>

👥 Groups : <code>{data['groups']}</code>

📢 Channels : <code>{data['channels']}</code>
"""
    )

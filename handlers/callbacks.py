#AxiomForceSub --by OwnerAxiom
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import CallbackQuery

from database.settings import get_force_sub


@Client.on_callback_query(filters.regex("^checksub$"))
async def check_sub(client: Client, query: CallbackQuery):

    force = await get_force_sub()

    if not force:
        return await query.answer(
            "Force Subscribe Disabled.",
            show_alert=True
        )

    try:

        member = await client.get_chat_member(
            force,
            query.from_user.id
        )

        if member.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        ):

            await query.message.edit_text(
                f"""
✅ Thank you {query.from_user.mention}.

Subscription Verified.

Now send /start
"""
            )

            return

    except:
        pass

    await query.answer(
        "❌ You haven't joined yet.",
        show_alert=True
    )

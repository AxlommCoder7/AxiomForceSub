#AxiomForceSub --by OwnerAxiom
from pyrogram import Client, filters
from pyrogram.errors import (
    FloodWait,
    UserIsBlocked,
    InputUserDeactivated,
    PeerIdInvalid
)

import asyncio

from config import OWNER_ID

from database.users import (
    get_users,
    del_user
)

from database.groups import (
    get_groups,
    del_group
)

from database.channels import (
    get_channels,
    del_channel
)


async def send_to_users(client, message, reply):

    success = 0
    failed = 0

    async for user in get_users():

        try:

            msg = await reply.copy(user)

            try:
                await msg.pin()
            except:
                pass

            success += 1

        except FloodWait as e:

            await asyncio.sleep(e.value)

        except (
            UserIsBlocked,
            InputUserDeactivated,
            PeerIdInvalid
        ):

            await del_user(user)

            failed += 1

        except Exception:

            failed += 1

    return success, failed


async def send_to_groups(client, message, reply):

    success = 0
    failed = 0

    async for chat in get_groups():

        try:

            msg = await reply.copy(chat)

            try:
                await msg.pin()
            except:
                pass

            success += 1

        except Exception:

            await del_group(chat)

            failed += 1

    return success, failed


async def send_to_channels(client, message, reply):

    success = 0
    failed = 0

    async for chat in get_channels():

        try:

            msg = await reply.copy(chat)

            try:
                await msg.pin()
            except:
                pass

            success += 1

        except Exception:

            await del_channel(chat)

            failed += 1

    return success, failed


@Client.on_message(filters.private & filters.command("broadcast"))
async def broadcast(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if not message.reply_to_message:

        return await message.reply_text(
            "Reply to any message.\n\n"
            "/broadcast users\n"
            "/broadcast groups\n"
            "/broadcast channels\n"
            "/broadcast all"
        )

    if len(message.command) != 2:

        return await message.reply_text(
            "Choose users/groups/channels/all"
        )

    target = message.command[1].lower()

    status = await message.reply_text(
        "📤 Broadcast Started..."
    )

    total_success = 0
    total_failed = 0

    if target == "users":

        s, f = await send_to_users(
            client,
            message,
            message.reply_to_message
        )

        total_success += s
        total_failed += f

    elif target == "groups":

        s, f = await send_to_groups(
            client,
            message,
            message.reply_to_message
        )

        total_success += s
        total_failed += f

    elif target == "channels":

        s, f = await send_to_channels(
            client,
            message,
            message.reply_to_message
        )

        total_success += s
        total_failed += f

    elif target == "all":

        s, f = await send_to_users(
            client,
            message,
            message.reply_to_message
        )

        total_success += s
        total_failed += f

        s, f = await send_to_groups(
            client,
            message,
            message.reply_to_message
        )

        total_success += s
        total_failed += f

        s, f = await send_to_channels(
            client,
            message,
            message.reply_to_message
        )

        total_success += s
        total_failed += f

    else:

        return await status.edit_text(
            "Invalid Target."
        )

    await status.edit_text(
        f"""
✅ Broadcast Completed

Success : {total_success}

Failed : {total_failed}
"""
    )

import asyncio
import time

from pyrogram import Client, filters
from pyrogram.errors import (
    FloodWait,
    UserIsBlocked,
    InputUserDeactivated,
    PeerIdInvalid,
    ChatWriteForbidden,
    ChatAdminRequired
)

from config import OWNER_ID
from database.users import (
    get_users,
    delete_user
)
from database.groups import (
    get_groups,
    delete_group
)
from database.channels import (
    get_channels,
    delete_channel
)
from utils.logger import send_log


# ==========================================================
# Broadcast Engine
# ==========================================================


class Broadcaster:

    def __init__(self):

        self.success = 0

        self.failed = 0

        self.deleted = 0

        self.total = 0

        self.start_time = time.time()

    async def flood(self, seconds):

        await asyncio.sleep(seconds)

    async def send(self, client, chat_id, msg):

        try:

            copied = await msg.copy(chat_id)

            try:

                await copied.pin(
                    disable_notification=True
                )

            except Exception:

                pass

            self.success += 1

            return True

        except FloodWait as e:

            await self.flood(e.value)

            return await self.send(
                client,
                chat_id,
                msg
            )

        except (
            UserIsBlocked,
            InputUserDeactivated,
            PeerIdInvalid
        ):

            self.deleted += 1

            return False

        except (
            ChatWriteForbidden,
            ChatAdminRequired
        ):

            self.failed += 1

            return False

        except Exception:

            self.failed += 1

            return False


broadcaster = Broadcaster()


# ==========================================================
# Users
# ==========================================================


async def broadcast_users(
    client,
    message
):

    broadcaster.success = 0

    broadcaster.failed = 0

    broadcaster.deleted = 0

    broadcaster.total = 0

    async for user in get_users():

        broadcaster.total += 1

        ok = await broadcaster.send(
            client,
            user,
            message
        )

        if not ok:

            try:

                await delete_user(user)

            except Exception:

                pass

    return {
        "success": broadcaster.success,
        "failed": broadcaster.failed,
        "deleted": broadcaster.deleted,
        "total": broadcaster.total
    }

# ==========================================================
# Groups
# ==========================================================


async def broadcast_groups(
    client,
    message
):

    broadcaster.success = 0

    broadcaster.failed = 0

    broadcaster.deleted = 0

    broadcaster.total = 0

    async for group in get_groups():

        broadcaster.total += 1

        ok = await broadcaster.send(
            client,
            group,
            message
        )

        if not ok:

            try:

                await delete_group(group)

            except Exception:

                pass

    return {
        "success": broadcaster.success,
        "failed": broadcaster.failed,
        "deleted": broadcaster.deleted,
        "total": broadcaster.total
    }


# ==========================================================
# Channels
# ==========================================================


async def broadcast_channels(
    client,
    message
):

    broadcaster.success = 0

    broadcaster.failed = 0

    broadcaster.deleted = 0

    broadcaster.total = 0

    async for channel in get_channels():

        broadcaster.total += 1

        ok = await broadcaster.send(
            client,
            channel,
            message
        )

        if not ok:

            try:

                await delete_channel(channel)

            except Exception:

                pass

    return {
        "success": broadcaster.success,
        "failed": broadcaster.failed,
        "deleted": broadcaster.deleted,
        "total": broadcaster.total
    }


# ==========================================================
# Progress Updater
# ==========================================================


async def update_progress(
    status,
    title,
    done,
    total
):

    try:

        percent = 0

        if total != 0:

            percent = round(
                (done / total) * 100,
                2
            )

        await status.edit_text(
            f"""
📢 <b>{title}</b>

<b>Processed :</b> {done}/{total}

<b>Success :</b> {broadcaster.success}

<b>Failed :</b> {broadcaster.failed}

<b>Deleted :</b> {broadcaster.deleted}

<b>Progress :</b> {percent} %
"""
        )

    except Exception:

        pass


# ==========================================================
# Final Report
# ==========================================================


def build_report(title):

    taken = round(
        time.time() - broadcaster.start_time,
        2
    )

    return f"""
✅ <b>{title}</b>

━━━━━━━━━━━━━━━

👤 <b>Total :</b> {broadcaster.total}

✅ <b>Success :</b> {broadcaster.success}

❌ <b>Failed :</b> {broadcaster.failed}

🗑 <b>Removed :</b> {broadcaster.deleted}

⏱ <b>Time :</b> {taken} sec
"""


# ==========================================================
# Logger Helper
# ==========================================================


async def log_broadcast(
    mode,
    report
):

    try:

        await send_log(
            f"""
📣 <b>Broadcast Completed</b>

<b>Mode :</b> {mode}

{report}
"""
        )

    except Exception:

        pass

# ==========================================================
# Broadcast Command
# ==========================================================


@Client.on_message(
    filters.private &
    filters.command("broadcast")
)
async def broadcast_handler(
    client,
    message
):

    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) != 2:

        return await message.reply_text(
            """
Usage:

/broadcast users

/broadcast groups

/broadcast channels

/broadcast all

Reply to a message.
"""
        )

    if not message.reply_to_message:

        return await message.reply_text(
            "Reply to a message first."
        )

    mode = message.command[1].lower()

    status = await message.reply_text(
        "📢 Broadcast Started..."
    )

    broadcaster.start_time = time.time()

    source = message.reply_to_message

    # ----------------------------------
    # Users
    # ----------------------------------

    if mode == "users":

        result = await broadcast_users(
            client,
            source
        )

        report = build_report(
            "Users Broadcast"
        )

        await status.edit_text(
            report
        )

        await log_broadcast(
            "Users",
            report
        )

        return

    # ----------------------------------
    # Groups
    # ----------------------------------

    if mode == "groups":

        result = await broadcast_groups(
            client,
            source
        )

        report = build_report(
            "Groups Broadcast"
        )

        await status.edit_text(
            report
        )

        await log_broadcast(
            "Groups",
            report
        )

        return

    # ----------------------------------
    # Channels
    # ----------------------------------

    if mode == "channels":

        result = await broadcast_channels(
            client,
            source
        )

        report = build_report(
            "Channels Broadcast"
        )

        await status.edit_text(
            report
        )

        await log_broadcast(
            "Channels",
            report
        )

        return

    # ----------------------------------
    # All
    # ----------------------------------

    if mode == "all":

        broadcaster.success = 0
        broadcaster.failed = 0
        broadcaster.deleted = 0
        broadcaster.total = 0

        users = await broadcast_users(
            client,
            source
        )

        groups = await broadcast_groups(
            client,
            source
        )

        channels = await broadcast_channels(
            client,
            source
        )

        broadcaster.success = (
            users["success"]
            + groups["success"]
            + channels["success"]
        )

        broadcaster.failed = (
            users["failed"]
            + groups["failed"]
            + channels["failed"]
        )

        broadcaster.deleted = (
            users["deleted"]
            + groups["deleted"]
            + channels["deleted"]
        )

        broadcaster.total = (
            users["total"]
            + groups["total"]
            + channels["total"]
        )

        report = build_report(
            "Global Broadcast"
        )

        await status.edit_text(
            report
        )

        await log_broadcast(
            "All",
            report
        )

        return

    # ----------------------------------
    # Invalid
    # ----------------------------------

    await status.edit_text(
        """
Invalid Target.

Available:

users
groups
channels
all
"""
    )

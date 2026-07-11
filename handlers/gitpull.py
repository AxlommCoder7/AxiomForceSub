import asyncio
import os
import subprocess

from pyrogram import Client, filters

from config import (
    OWNER_ID,
    GIT_BRANCH
)

from utils.logger import send_log


# ==========================================
# Run Shell
# ==========================================

async def run(cmd: str):

    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    out = stdout.decode().strip()

    err = stderr.decode().strip()

    return process.returncode, out, err


# ==========================================
# Git Status
# ==========================================

@Client.on_message(
    filters.private &
    filters.command("gitstatus")
)
async def git_status(client, message):

    if message.from_user.id != OWNER_ID:
        return

    code, out, err = await run(
        "git status"
    )

    if code != 0:

        return await message.reply_text(
            f"<pre>{err}</pre>"
        )

    if len(out) > 3900:
        out = out[:3900]

    await message.reply_text(
        f"<pre>{out}</pre>"
    )


# ==========================================
# Git Pull
# ==========================================

@Client.on_message(
    filters.private &
    filters.command("gitpull")
)
async def git_pull(client, message):

    if message.from_user.id != OWNER_ID:
        return

    msg = await message.reply_text(
        "🔄 Checking GitHub..."
    )

    await send_log(
        "🔄 Git Pull Started."
    )

    code, out, err = await run(
        f"git pull origin {GIT_BRANCH}"
    )

    if code != 0:

        await msg.edit_text(
            f"""
❌ Git Pull Failed

<pre>{err}</pre>
"""
        )

        await send_log(
            f"❌ Git Pull Failed\n\n{err}"
        )

        return

    await msg.edit_text(
        f"""
✅ Git Pull Successful

<pre>{out}</pre>
"""
    )

    await send_log(
        "✅ Git Pull Completed."
    )


# ==========================================
# Git Log
# ==========================================

@Client.on_message(
    filters.private &
    filters.command("gitlog")
)
async def git_log(client, message):

    if message.from_user.id != OWNER_ID:
        return

    code, out, err = await run(
        "git log --oneline -10"
    )

    if code != 0:

        return await message.reply_text(
            err
        )

    await message.reply_text(
        f"<pre>{out}</pre>"
    )

import os
import signal

# ==========================================
# Git Reset
# ==========================================

@Client.on_message(
    filters.private &
    filters.command("gitreset")
)
async def git_reset(client, message):

    if message.from_user.id != OWNER_ID:
        return

    msg = await message.reply_text(
        "♻ Resetting Repository..."
    )

    code, out, err = await run(
        f"git reset --hard origin/{GIT_BRANCH}"
    )

    if code != 0:

        return await msg.edit_text(
            f"""
❌ Reset Failed

<pre>{err}</pre>
"""
        )

    await send_log(
        "♻ Git Reset Completed."
    )

    await msg.edit_text(
        f"""
✅ Repository Reset

<pre>{out}</pre>
"""
    )


# ==========================================
# Latest Commit
# ==========================================

@Client.on_message(
    filters.private &
    filters.command("commit")
)
async def latest_commit(client, message):

    if message.from_user.id != OWNER_ID:
        return

    code, out, err = await run(
        "git log -1 --pretty=format:'%H%n%an%n%ad%n%s'"
    )

    if code != 0:

        return await message.reply_text(err)

    commit = out.split("\n")

    if len(commit) < 4:
        return await message.reply_text("Unable to fetch commit.")

    await message.reply_text(
f"""
📝 <b>Latest Commit</b>

<b>Hash</b>

<code>{commit[0]}</code>

<b>Author</b>

{commit[1]}

<b>Date</b>

{commit[2]}

<b>Message</b>

{commit[3]}
"""
    )


# ==========================================
# Branch
# ==========================================

@Client.on_message(
    filters.private &
    filters.command("branch")
)
async def branch(client, message):

    if message.from_user.id != OWNER_ID:
        return

    code, out, err = await run(
        "git branch --show-current"
    )

    if code != 0:

        return await message.reply_text(err)

    await message.reply_text(
        f"""
🌿 Current Branch

<code>{out}</code>
"""
    )


# ==========================================
# Update
# ==========================================

@Client.on_message(
    filters.private &
    filters.command("update")
)
async def update(client, message):

    if message.from_user.id != OWNER_ID:
        return

    msg = await message.reply_text(
        "🚀 Updating..."
    )

    code, out, err = await run(
        f"git pull origin {GIT_BRANCH}"
    )

    if code != 0:

        return await msg.edit_text(
            f"""
❌ Update Failed

<pre>{err}</pre>
"""
        )

    await send_log(
        "🚀 Update Successful.\nRestarting..."
    )

    await msg.edit_text(
"""
✅ Update Complete

♻ Restarting Bot...
"""
    )

    os.kill(
        os.getpid(),
        signal.SIGINT
    )
    

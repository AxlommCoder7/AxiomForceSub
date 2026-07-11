import asyncio
import os
import platform
import signal
import subprocess
import time
import psutil

from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID
from utils.logger import send_log

START_TIME = time.time()


def owner(func):
    async def wrapper(client, message):
        if not message.from_user:
            return

        if message.from_user.id != OWNER_ID:
            return

        return await func(client, message)

    return wrapper


# ------------------------------------------------
# Admin Panel
# ------------------------------------------------

@Client.on_message(filters.private & filters.command("admin"))
@owner
async def admin_panel(client: Client, message: Message):

    text = f"""
👑 <b>Admin Panel</b>

<b>Available Commands</b>

/stats
/logs
/gitpull
/restart
/ping
/system
/uptime
/sh
/eval
/setfsub
/removefsub
/fsub
/broadcast
"""

    await message.reply_text(text)


# ------------------------------------------------
# Ping
# ------------------------------------------------

@Client.on_message(filters.private & filters.command("ping"))
@owner
async def ping(client: Client, message: Message):

    start = time.perf_counter()

    msg = await message.reply_text(
        "🏓 Pinging..."
    )

    end = time.perf_counter()

    ms = round(
        (end - start) * 1000,
        2
    )

    await msg.edit_text(
        f"🏓 Pong!\n\n⚡ {ms} ms"
    )


# ------------------------------------------------
# Uptime
# ------------------------------------------------

@Client.on_message(filters.private & filters.command("uptime"))
@owner
async def uptime(client, message):

    sec = int(time.time() - START_TIME)

    d = sec // 86400
    h = (sec % 86400) // 3600
    m = (sec % 3600) // 60
    s = sec % 60

    await message.reply_text(
        f"⏳ Uptime\n\n{d}d {h}h {m}m {s}s"
    )


# ------------------------------------------------
# System
# ------------------------------------------------

@Client.on_message(filters.private & filters.command("system"))
@owner
async def system(client, message):

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    disk = psutil.disk_usage("/").percent

    txt = f"""
🖥 <b>System Information</b>

OS : {platform.system()}

Release : {platform.release()}

CPU : {cpu} %

RAM : {ram} %

Disk : {disk} %
"""

    await message.reply_text(txt)


# ------------------------------------------------
# Restart
# ------------------------------------------------

@Client.on_message(filters.private & filters.command("restart"))
@owner
async def restart(client, message):

    await send_log(
        "♻ Bot Restart Requested."
    )

    msg = await message.reply_text(
        "♻ Restarting..."
    )

    await asyncio.sleep(2)

    await msg.edit_text(
        "✅ Restart Signal Sent."
    )

    os.kill(
        os.getpid(),
        signal.SIGINT
    )


# ------------------------------------------------
# Shell
# ------------------------------------------------

@Client.on_message(filters.private & filters.command("sh"))
@owner
async def shell(client, message):

    if len(message.command) == 1:

        return await message.reply_text(
            "/sh command"
        )

    cmd = message.text.split(
        None,
        1
    )[1]

    try:

        output = subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True
        )

    except subprocess.CalledProcessError as e:

        output = e.output

    if not output:
        output = "Done."

    if len(output) > 3900:
        output = output[:3900]

    await message.reply_text(
        f"<pre>{output}</pre>"
    )


# ------------------------------------------------
# Eval
# ------------------------------------------------

@Client.on_message(filters.private & filters.command("eval"))
@owner
async def eval_python(client, message):

    if len(message.command) == 1:

        return await message.reply_text(
            "/eval python_code"
        )

    code = message.text.split(
        None,
        1
    )[1]

    env = {
        "client": client,
        "message": message,
        "asyncio": asyncio,
        "__builtins__": __builtins__
    }

    try:

        exec(
            f"async def __func__():\n"
            + "\n".join(
                f"    {i}"
                for i in code.split("\n")
            ),
            env
        )

        result = await env["__func__"]()

        if result is None:
            result = "Success."

    except Exception as e:

        result = str(e)

    if len(str(result)) > 3900:
        result = str(result)[:3900]

    await message.reply_text(
        f"<pre>{result}</pre>"
    )

import os
import shutil
import zipfile
from datetime import datetime

from pyrogram import Client, filters

from config import OWNER_ID
from utils.logger import send_log

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "bot.log")


# =====================================================
# /logs
# =====================================================

@Client.on_message(
    filters.private &
    filters.command("logs")
)
async def logs_handler(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if not os.path.exists(LOG_DIR):

        return await message.reply_text(
            "❌ Log directory not found."
        )

    files = []

    for file in os.listdir(LOG_DIR):

        path = os.path.join(LOG_DIR, file)

        if os.path.isfile(path):

            files.append(path)

    if len(files) == 0:

        return await message.reply_text(
            "No log files found."
        )

    # -------------------------
    # One Log
    # -------------------------

    if len(files) == 1:

        await message.reply_document(
            files[0],
            caption="📄 Latest Log"
        )

        return

    # -------------------------
    # Zip All Logs
    # -------------------------

    zip_name = "logs.zip"

    if os.path.exists(zip_name):

        os.remove(zip_name)

    with zipfile.ZipFile(
        zip_name,
        "w",
        zipfile.ZIP_DEFLATED
    ) as archive:

        for file in files:

            archive.write(
                file,
                arcname=os.path.basename(file)
            )

    await message.reply_document(
        zip_name,
        caption="📦 All Log Files"
    )

    os.remove(zip_name)


# =====================================================
# /clearlogs
# =====================================================

@Client.on_message(
    filters.private &
    filters.command("clearlogs")
)
async def clear_logs(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if not os.path.exists(LOG_DIR):

        return await message.reply_text(
            "Log Folder Missing."
        )

    removed = 0

    for file in os.listdir(LOG_DIR):

        path = os.path.join(LOG_DIR, file)

        try:

            if os.path.isfile(path):

                os.remove(path)

                removed += 1

        except:

            pass

    os.makedirs(LOG_DIR, exist_ok=True)

    open(LOG_FILE, "a").close()

    await send_log(
        f"🗑 Logs Cleared\n\nFiles Removed : {removed}"
    )

    await message.reply_text(
        f"✅ Cleared {removed} Log Files."
    )


# =====================================================
# /logsize
# =====================================================

@Client.on_message(
    filters.private &
    filters.command("logsize")
)
async def log_size(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if not os.path.exists(LOG_FILE):

        return await message.reply_text(
            "No Log File."
        )

    size = os.path.getsize(LOG_FILE)

    kb = round(size / 1024, 2)

    mb = round(kb / 1024, 2)

    await message.reply_text(
        f"""
📄 Log Information

Size :

{kb} KB

{mb} MB
"""
    )


# =====================================================
# /newlog
# =====================================================

@Client.on_message(
    filters.private &
    filters.command("newlog")
)
async def new_log(client, message):

    if message.from_user.id != OWNER_ID:
        return

    if os.path.exists(LOG_FILE):

        stamp = datetime.now().strftime(
            "%d%m%Y_%H%M%S"
        )

        backup = os.path.join(
            LOG_DIR,
            f"bot_{stamp}.log"
        )

        shutil.copy(
            LOG_FILE,
            backup
        )

        open(
            LOG_FILE,
            "w"
        ).close()

        await send_log(
            "📄 New Log File Created."
        )

        return await message.reply_text(
            "✅ New Log Started."
        )

    open(LOG_FILE, "a").close()

    await message.reply_text(
        "Log Created."
    )

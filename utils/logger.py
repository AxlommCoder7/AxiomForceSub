import logging
import os
from logging.handlers import RotatingFileHandler

from config import LOGGER_ID
from loader import app

# ===================================================
# Log Directory
# ===================================================

LOG_DIR = "logs"

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

LOG_FILE = os.path.join(
    LOG_DIR,
    "bot.log"
)

# ===================================================
# Logger
# ===================================================

LOGGER = logging.getLogger("AxiomForceSub")

LOGGER.setLevel(logging.INFO)

FORMAT = logging.Formatter(
    "[%(asctime)s] | %(levelname)s | %(name)s | %(message)s",
    "%d-%m-%Y %H:%M:%S"
)

FILE_HANDLER = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10 * 1024 * 1024,
    backupCount=10,
    encoding="utf-8"
)

FILE_HANDLER.setFormatter(FORMAT)

CONSOLE = logging.StreamHandler()

CONSOLE.setFormatter(FORMAT)

if not LOGGER.handlers:

    LOGGER.addHandler(FILE_HANDLER)

    LOGGER.addHandler(CONSOLE)


# ===================================================
# Logger Methods
# ===================================================

def info(text):

    LOGGER.info(text)


def warning(text):

    LOGGER.warning(text)


def error(text):

    LOGGER.error(text)


def critical(text):

    LOGGER.critical(text)


def exception(text):

    LOGGER.exception(text)


# ===================================================
# Telegram Logger
# ===================================================

async def send_log(
    text: str,
    disable_notification: bool = True
):

    if not LOGGER_ID:
        return

    try:

        if len(text) > 4000:
            text = text[:3990]

        await app.send_message(
            chat_id=LOGGER_ID,
            text=text,
            disable_web_page_preview=True,
            disable_notification=disable_notification,
        )

    except Exception as e:

        LOGGER.error(
            f"Telegram Logger Error : {e}"
        )


# ===================================================
# Startup / Shutdown
# ===================================================

async def startup_log():

    await send_log(
        "🟢 <b>Axiom ForceSub Started Successfully.</b>"
    )


async def shutdown_log():

    await send_log(
        "🔴 <b>Axiom ForceSub Stopped.</b>"
    )


# ===================================================
# Error Logger
# ===================================================

async def log_exception(exc):

    text = f"""
🚨 <b>Unhandled Exception</b>

<pre>{exc}</pre>
"""

    await send_log(text)

    LOGGER.exception(exc)

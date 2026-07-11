#AxiomForceSub --by OwnerAxiom
import logging
import traceback

from loader import app
from config import LOGGER_ID

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger("AxiomManagerBot")


async def send_log(text: str):

    try:
        await app.send_message(
            LOGGER_ID,
            text,
            disable_web_page_preview=True
        )
    except Exception:
        LOGGER.exception("Failed to send logger message.")


async def send_error(error: Exception):

    err = "".join(
        traceback.format_exception(
            type(error),
            error,
            error.__traceback__
        )
    )

    if len(err) > 3900:
        err = err[:3900]

    try:

        await app.send_message(
            LOGGER_ID,
            f"🚨 **Bot Error**\n\n```{err}```"
        )

    except Exception:

        LOGGER.exception("Unable to send error log.")

#AxiomForceSub --by OwnerAxiom
import asyncio
import importlib
import logging
import pkgutil
import traceback

from pyrogram import idle

from loader import app, mongo
from config import LOGGER_ID

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s : %(message)s"
)

LOGGER = logging.getLogger("AxiomForceSub")


# -----------------------------
# Load All Handlers
# -----------------------------

def load_plugins():
    import handlers

    for module in pkgutil.iter_modules(handlers.__path__):
        importlib.import_module(f"handlers.{module.name}")
        LOGGER.info(f"Loaded -> handlers.{module.name}")


# -----------------------------
# Startup
# -----------------------------

async def startup():

    try:
        await mongo.admin.command("ping")
        LOGGER.info("MongoDB Connected")

    except Exception as e:
        LOGGER.error(e)
        raise SystemExit

    me = await app.get_me()

    LOGGER.info(f"Bot : @{me.username}")
    LOGGER.info(f"ID  : {me.id}")

    if LOGGER_ID:

        try:

            await app.send_message(
                LOGGER_ID,
                f"""
🟢 <b>Bot Started</b>

<b>Name :</b> {me.first_name}

<b>Username :</b> @{me.username}

<b>ID :</b> <code>{me.id}</code>
"""
            )

        except Exception:

            pass


# -----------------------------
# Shutdown
# -----------------------------

async def shutdown():

    LOGGER.info("Stopping...")

    if LOGGER_ID:

        try:

            await app.send_message(
                LOGGER_ID,
                "🔴 <b>Bot Stopped.</b>"
            )

        except Exception:

            pass

    mongo.close()


# -----------------------------
# Main
# -----------------------------

async def main():

    load_plugins()

    await app.start()

    await startup()

    LOGGER.info("Bot Running...")

    await idle()

    await shutdown()

    await app.stop()


if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        LOGGER.info("Stopped By Keyboard.")

    except Exception:

        LOGGER.error(traceback.format_exc())

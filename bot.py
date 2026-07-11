#AxiomForceSub --by OwnerAxiom
from loader import app

from utils.logger import LOGGER, send_log

import handlers.start
import handlers.callbacks
import handlers.force_sub
import handlers.broadcast
import handlers.admin
import handlers.logs
import handlers.stats
import handlers.gitpull


async def startup():

    LOGGER.info("Bot Started")

    await send_log(
        "🟢 **Bot Started Successfully**"
    )


async def shutdown():

    LOGGER.info("Bot Stopped")

    await send_log(
        "🔴 **Bot Stopped**"
    )


app.start()

app.loop.run_until_complete(
    startup()
)

LOGGER.info("Bot Running...")

app.idle()

app.loop.run_until_complete(
    shutdown()
)

app.stop()

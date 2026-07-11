#AxiomForceSub --by OwnerAxiom
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from pyrogram.enums import ParseMode

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    MONGO_URI,
)

# -----------------------------
# Pyrogram Client
# -----------------------------

app = Client(
    name="AxiomForceSub",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML,
    workers=100,
    sleep_threshold=30,
    in_memory=False,
)

# -----------------------------
# MongoDB
# -----------------------------

mongo = AsyncIOMotorClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
)

db = mongo["AxiomForceSub"]

# Collections

usersdb = db["users"]

groupsdb = db["groups"]

channelsdb = db["channels"]

settingsdb = db["settings"]

botsdb = db["bots"]

broadcastdb = db["broadcast"]

logsdb = db["logs"]

statsdb = db["stats"]

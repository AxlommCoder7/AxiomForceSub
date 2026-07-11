#AxiomForceSub --by OwnerAxiom
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient

from config import *

app = Client(
    "AxiomManagerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["AxiomManagerBot"]

from datetime import datetime

from .mongo import BOTS


# ==========================================================
# Create Bot
# ==========================================================

async def create_bot(
    owner_id: int,
    bot_id: int,
    username: str,
    first_name: str,
    token: str
):

    await BOTS.update_one(
        {
            "bot_id": bot_id
        },
        {
            "$set": {
                "owner_id": owner_id,
                "bot_id": bot_id,
                "username": username.lower(),
                "first_name": first_name,
                "token": token,

                "force_sub": None,
                "logger": None,

                "admins": [
                    owner_id
                ],

                "created_at": datetime.utcnow(),

                "active": True
            }
        },
        upsert=True
    )


# ==========================================================
# Exists
# ==========================================================

async def bot_exists(bot_id):

    return await BOTS.find_one(
        {
            "bot_id": bot_id
        }
    )


# ==========================================================
# Owner Bots
# ==========================================================

async def owner_bots(owner):

    bots = []

    async for bot in BOTS.find(
        {
            "owner_id": owner
        }
    ):

        bots.append(bot)

    return bots


# ==========================================================
# Get Bot
# ==========================================================

async def get_bot(bot_id):

    return await BOTS.find_one(
        {
            "bot_id": bot_id
        }
    )


# ==========================================================
# Delete
# ==========================================================

async def delete_bot(bot_id):

    await BOTS.delete_one(
        {
            "bot_id": bot_id
        }
    )


# ==========================================================
# Force Subscribe
# ==========================================================

async def set_force(bot_id, chat):

    await BOTS.update_one(
        {
            "bot_id": bot_id
        },
        {
            "$set": {
                "force_sub": chat
            }
        }
    )


async def get_force(bot_id):

    bot = await get_bot(bot_id)

    if bot:

        return bot.get(
            "force_sub"
        )

    return None


# ==========================================================
# Logger
# ==========================================================

async def set_logger(bot_id, logger):

    await BOTS.update_one(
        {
            "bot_id": bot_id
        },
        {
            "$set": {
                "logger": logger
            }
        }
    )


async def get_logger(bot_id):

    bot = await get_bot(bot_id)

    if bot:

        return bot.get(
            "logger"
        )

    return None


# ==========================================================
# Admins
# ==========================================================

async def add_admin(bot_id, user):

    await BOTS.update_one(
        {
            "bot_id": bot_id
        },
        {
            "$addToSet": {
                "admins": user
            }
        }
    )


async def remove_admin(bot_id, user):

    await BOTS.update_one(
        {
            "bot_id": bot_id
        },
        {
            "$pull": {
                "admins": user
            }
        }
    )


async def admins(bot_id):

    bot = await get_bot(bot_id)

    if bot:

        return bot.get(
            "admins",
            []
        )

    return []


# ==========================================================
# Enable / Disable
# ==========================================================

async def enable(bot_id):

    await BOTS.update_one(
        {
            "bot_id": bot_id
        },
        {
            "$set": {
                "active": True
            }
        }
    )


async def disable(bot_id):

    await BOTS.update_one(
        {
            "bot_id": bot_id
        },
        {
            "$set": {
                "active": False
            }
        }
    )


# ==========================================================
# All Bots
# ==========================================================

async def all_bots():

    async for bot in BOTS.find():

        yield bot


async def total_bots():

    return await BOTS.count_documents({})

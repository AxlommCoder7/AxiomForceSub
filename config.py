#AxiomForceSub --by OwnerAxiom
import os
from dotenv import load_dotenv

load_dotenv()


def getenv(name: str, default=None, required=False):
    value = os.getenv(name, default)

    if required and (value is None or value == ""):
        raise ValueError(f"Missing required environment variable: {name}")

    return value


API_ID = int(getenv("API_ID", required=True))
API_HASH = getenv("API_HASH", required=True)
BOT_TOKEN = getenv("BOT_TOKEN", required=True)

OWNER_ID = int(getenv("OWNER_ID", required=True))
LOGGER_ID = int(getenv("LOGGER_ID", 0))

MONGO_URI = getenv("MONGO_URI", required=True)

FORCE_SUB = getenv("FORCE_SUB", "")

GIT_REPO = getenv("GIT_REPO", "")
GIT_BRANCH = getenv("GIT_BRANCH", "main")

BOT_NAME = getenv("BOT_NAME", "Axiom ForceSub")
BOT_USERNAME = getenv("BOT_USERNAME", "")

VERSION = "1.0.0"

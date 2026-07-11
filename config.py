#AxiomForceSub --by OwnerAxiom
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = int(os.getenv("OWNER_ID"))
LOGGER_ID = int(os.getenv("LOGGER_ID"))

MONGO_URI = os.getenv("MONGO_URI")

FORCE_SUB = os.getenv("FORCE_SUB")

GIT_REPO = os.getenv("GIT_REPO")
GIT_BRANCH = os.getenv("GIT_BRANCH", "main")

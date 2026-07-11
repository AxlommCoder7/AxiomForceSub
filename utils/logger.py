#AxiomForceSub --by OwnerAxiom
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger("AxiomManagerBot")

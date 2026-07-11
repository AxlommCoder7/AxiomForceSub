#AxiomForceSub --by OwnerAxiom
from functools import wraps

from config import OWNER_ID


def owner_only(func):

    @wraps(func)

    async def wrapper(client, message):

        if message.from_user.id != OWNER_ID:

            return

        return await func(client, message)

    return wrapper

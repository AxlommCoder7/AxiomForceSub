#AxiomForceSub --by OwnerAxiom
from .users import total_users
from .groups import total_groups
from .channels import total_channels


async def get_stats():
    return {
        "users": await total_users(),
        "groups": await total_groups(),
        "channels": await total_channels(),
    }

#AxiomForceSub --by OwnerAxiom
from pyrogram.enums import ChatType


def is_private(message):

    return message.chat.type == ChatType.PRIVATE


def is_group(message):

    return message.chat.type in (
        ChatType.GROUP,
        ChatType.SUPERGROUP
    )


def is_channel(message):

    return message.chat.type == ChatType.CHANNEL

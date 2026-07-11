#AxiomForceSub --by OwnerAxiom
import subprocess

from pyrogram import Client, filters

from config import OWNER_ID


@Client.on_message(filters.private & filters.command("gitpull"))
async def gitpull(client, message):

    if message.from_user.id != OWNER_ID:
        return

    msg = await message.reply_text(
        "🔄 Updating Repository..."
    )

    try:

        result = subprocess.check_output(
            "git pull",
            shell=True,
            stderr=subprocess.STDOUT
        ).decode()

    except Exception as e:

        result = str(e)

    if len(result) > 3900:
        result = result[:3900]

    await msg.edit_text(

f"""✅ Git Pull Finished

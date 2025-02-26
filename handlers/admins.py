from asyncio.queues import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message
from cache.admins import set
from helpers.decorators import authorized_users_only, errors
from helpers.channelmusic import get_chat_id
from helpers.filters import command, other_filters
from callsmusic import callsmusic, queues
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream


ACTV_CALLS = []

@Client.on_message(command(["pause"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await callsmusic.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("▶️ 𝐏𝐚𝐮𝐬𝐞 😔🥀")


@Client.on_message(command(["resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await callsmusic.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("⏸ 𝐑𝐞𝐬𝐮𝐦𝐞 ❤️")


@Client.on_message(command(["end"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        callsmusic.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await callsmusic.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("💞 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅ ᴀʏɪɴᴅʜɪ ✨")

@Client.on_message(command(["skip"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("❗ 𝐄𝐦𝐢 𝐥𝐞𝐝𝐡𝐮 𝐫𝐚 𝐧𝐢𝐛𝐛𝐚 𝐠𝐚😔 𝐒𝐤𝐢𝐩 🎶 𝐂𝐡𝐞𝐲𝐚𝐭𝐚𝐧𝐢𝐤𝐢 🥀")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        callsmusic.queues.get(chat_id)["file"],
                    ),
                ),
            )
    await message.reply_text("👉𝐄𝐩𝐩𝐮𝐝𝐮 𝐩𝐥𝐚𝐲 𝐚𝐲𝐢𝐭𝐡𝐮𝐧𝐚💫 𝐒𝐨𝐧𝐠 𝐍𝐢 ✨ 𝐒𝐤𝐢𝐩 𝐂𝐡𝐞𝐬𝐚 𝐜𝐡𝐚𝐥𝐚𝐛𝐚𝐝𝐚𝐯𝐚 😂")

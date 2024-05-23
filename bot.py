import os
from pyrogram import Client, filters
from datetime import datetime
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# Configs
API_HASH = os.environ['API_HASH']
APP_ID = int(os.environ['APP_ID'])
BOT_TOKEN = os.environ['BOT_TOKEN']
TRACK_CHANNEL = int(os.environ['TRACK_CHANNEL'])
OWNER_ID = os.environ['OWNER_ID']
#Button
START_BUTTONS=[
    [
        InlineKeyboardButton('𝙲𝚛𝚎𝚊𝚝𝚘𝚛🌟', url='https://t.me/fligher'),
        InlineKeyboardButton('𝚃𝚛𝚞𝚖𝙱𝚘𝚝𝚜🏆', url='https://t.me/movie_time_botonly'),
    ],
    [InlineKeyboardButton('𝙲𝚑𝚊𝚗𝚗𝚎𝚕𝚜🚨', url="https://t.me/+ExBm8lEipxRkMTA1")],
]
# Running bot
xbot = Client('File-Sharing', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Notify about bot start
with xbot:
    xbot_username = xbot.get_me().username  # Better call it global once due to telegram flood id
    Current_date = datetime. now(). date() 
    print("Bot started!",Current_date)
    xbot.send_message(int(OWNER_ID), "Bot started!")
    xbot.send_message(int(OWNER_ID), Current_date)

# Start & Get file
@xbot.on_message(filters.command('start') & filters.private)
async def _startfile(bot, update):
    if update.text == '/start':
        await update.reply_text(
            f"I'm File-Sharing!\nYou can share any telegram files and get the sharing link using this bot!\n\n  If You Send Singlefile you get single link or if you send a multiple file you get multiple files single link limit upto 100 \n\n/help for more details...",
            True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))
        return
    if len(update.command) != 2:
        return
    code = update.command[1]
    if '-' in code:
        msg_id = code.split('-')[-1]
        # due to new type of file_unique_id, it can contain "-" sign like "agadyruaas-puuo"
        unique_id = '-'.join(code.split('-')[0:-1])
        if not msg_id.isdigit():
            return
        try:  # If message not belong to media group raise exception
            check_media_group = await bot.get_media_group(TRACK_CHANNEL, int(msg_id))
            check = check_media_group[0]  # Because func return`s list obj
        except Exception:
            check = await bot.get_messages(TRACK_CHANNEL, int(msg_id))
        if check.empty:
            await update.reply_text('Error: [Message does not exist]\n/help for more details...')
            return
        if check.video:
            unique_idx = check.video.file_unique_id
        elif check.photo:
            unique_idx = check.photo.file_unique_id
        elif check.audio:
            unique_idx = check.audio.file_unique_id
        elif check.document:
            unique_idx = check.document.file_unique_id
        elif check.sticker:
            unique_idx = check.sticker.file_unique_id
        elif check.animation:
            unique_idx = check.animation.file_unique_id
        elif check.voice:
            unique_idx = check.voice.file_unique_id
        elif check.video_note:
            unique_idx = check.video_note.file_unique_id
        if unique_id != unique_idx.lower():
            return
        try:  # If message not belong to media group raise exception
            await bot.copy_media_group(update.from_user.id, TRACK_CHANNEL, int(msg_id))
        except Exception:
            await check.copy(update.from_user.id)
    else:
        return
# Help msg
@xbot.on_message(filters.command('help') & filters.private)
async def _help(bot, update):
    await update.reply_text("Supported file types:\n\n- Video\n- Audio\n- Photo\n- Document\n- Sticker\n- GIF\n- Voice note\n- Video note\n\n If bot didn't respond, contact @fligher", True)


async def __reply(update, copied):
    
    msg_id = copied.id
    if copied.video:
        unique_idx = copied.video.file_unique_id
    elif copied.photo:
        unique_idx = copied.photo.file_unique_id
    elif copied.audio:
        unique_idx = copied.audio.file_unique_id
    elif copied.document:
        unique_idx = copied.document.file_unique_id
    elif copied.sticker:
        unique_idx = copied.sticker.file_unique_id
    elif copied.animation:
        unique_idx = copied.animation.file_unique_id
    elif copied.voice:
        unique_idx = copied.voice.file_unique_id
    elif copied.video_note:
        unique_idx = copied.video_note.file_unique_id
    else:
        await copied.delete()
        return
    await update.reply_text(
        """Here is Your Sharing Link⬇️\n\nIf you don't want the link just click delete link🚮
       
        """,
        True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Sharing Link🔗',
                                  url=f'https://telegram.me/{xbot_username}?start={unique_idx.lower()}-{str(msg_id)}')],
            [InlineKeyboardButton('Delete Link🚮',
                                  callback_data="close"),
             InlineKeyboardButton('Share Link🪁',
                                  switch_inline_query=f'https://telegram.me/{xbot_username}?start={unique_idx.lower()}-{str(msg_id)}')]
            
        ])
    )
     
@xbot.on_callback_query()
async def close_button_handler(bot,callback_query):
     if callback_query.data == "close":
        # Delete the message
        await bot.delete_messages(callback_query.message.chat.id, callback_query.message.id)
    
# Store media_group
media_group_id = 0
@xbot.on_message(filters.media & filters.private & filters.media_group)
async def _main_grop(bot, update):
    global media_group_id
    # if OWNER_ID == 'all':
    #     pass
    # elif int(OWNER_ID) == update.from_user.id:
    #     pass
    # else:
    #     return

    if int(media_group_id) != int(update.media_group_id):
        media_group_id = update.media_group_id
        copied = (await bot.copy_media_group(TRACK_CHANNEL, update.from_user.id, update.id))[0]
        copied = (await bot.copy_media_group(TRACK_CHANNEL, update.from_user.id, update.id))[0]
        
        await __reply(update, copied)

    else:
        # This handler catch EVERY message with [update.media_group_id] param
        # So we should ignore next >1_media_group_id messages
        return
# Store file
@xbot.on_message(filters.media & filters.private & ~filters.media_group)
async def _main(bot, update):
    # if OWNER_ID == 'all':
    #     pass
    # elif int(OWNER_ID) == update.from_user.id:
    #     pass
    # else:
    #     return
    copied = await update.copy(TRACK_CHANNEL)
    await __reply(update,copied)

xbot.run()

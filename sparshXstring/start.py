from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import OWNER_ID

# Define home_ques and home_buttons
home_ques = """ʜᴇʟʟᴏ {msg.from_user.mention},

✨ ɪɴᴛʀᴏᴅᴜᴄɪɴɢ {me2} - ᴛʜᴇ ᴇɴɪɢᴍᴧᴛɪᴄ sᴛʀɪɴɢ ɢᴇɴᴇʀᴧᴛᴏʀ ʙᴏᴛ! ✨
🔐 ᴜɴʟᴏᴄᴋ ᴛʜᴇ ᴍʏsᴛᴇʀɪᴇs ᴏғ sᴛʀɪɴɢ ɢᴇɴᴇʀᴧᴛɪᴏɴ!
🌌 sʟᴇᴇᴋ. ᴇʟᴇɢᴧɴᴛ. ᴛɪᴍᴇʟᴇss.

🎨 ᴄʀᴇᴧᴛᴇᴅ ʙʏ: [⏤͟͞ 𝙈𝘼𝘼𝙔𝘼𝙑𝙄 𝙃𝙐 𝙈𝙀](tg://user?id={OWNER_ID}) !"""

home_buttons = [
    [
        InlineKeyboardButton(text="ɢᴇɴᴇʀᴧᴛᴇ sᴛʀɪɴɢ", callback_data="generate")
    ],
    [
        InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/destinybots"),
        InlineKeyboardButton("ᴄʜᴧɴɴᴇʟ", url="https://t.me/destinybots")
    ]
]

# Start command handler
@Client.on_message(filters.command("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=home_ques.format(msg=msg, me2=me2, OWNER_ID=OWNER_ID),  # Added OWNER_ID here
        reply_markup=InlineKeyboardMarkup(home_buttons),
        disable_web_page_preview=True,
    )

# Home button callback handler
@Client.on_callback_query(filters.regex(pattern=r"^home$"))
async def home_callback(bot: Client, callback_query: CallbackQuery):
    # Acknowledge the callback query
    await callback_query.answer()

    # Edit the current message to show the main menu
    await callback_query.message.edit_text(
        home_ques.format(msg=callback_query.message, me2=(await bot.get_me()).mention, OWNER_ID=OWNER_ID),  # Added OWNER_ID here
        reply_markup=InlineKeyboardMarkup(home_buttons)
    )

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot.client import app
from bot.database import files_col
from bot.utils.stats import is_served_user
from config import settings
from bot.utils.telegram_api import TelegramAPI

@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    args = message.text.split()[1:]
    if args:
        try:
            if not await is_served_user(message.chat.id):
                await files_col.insert_one({"user_id": message.chat.id})
        except Exception:
            pass
        uuid = args[0]
        try:
            record = await files_col.find_one({"uuid": uuid})
        except Exception:
            await message.reply("❌ Database unavailable. Please try again in a moment.")
            return
        if not record:
            await message.reply("❌ File not found or expired.")
            return
        copied = await TelegramAPI().copy_message(
            chat_id=message.chat.id,
            from_chat_id=settings.STORAGE_CHANNEL_ID,
            message_id=record["file_msg_id"],
        )
        if not copied:
            await message.reply("❌ Failed to fetch the file. Please try again later.")
    else:
        try:
            if not await is_served_user(message.chat.id):
                await files_col.insert_one({"user_id": message.chat.id})
        except Exception:
            pass
        board = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📢 Updates Channel", url="https://t.me/Private_Bots"
                    ),
                ]
            ]
        )
        await message.reply_photo(
            photo="start.jpg",
            caption="<b>👋 Welcome to <u>FileDrawer Bot</u>!</b>\n\n"
            "🗂️ <b>Store</b> your files securely and access them anytime!\n"
            "🔲 <b>QRify</b> bot also provides the QR code to share your file.\n"
            "🔗 <b>Share</b> files with friends using unique links.\n\n"
            "✨ <b>How to use:</b>\n"
            "• <b>Send me any file</b> to store it.\n"
            "• Use <code>/list</code> to see your files.\n"
            "• Use <code>/delete &lt;FILE_UUID&gt;</code> to remove a file.\n"
            "• Use <code>/help</code> for all commands.\n\n"
            "🚀 <i>Start by sending a file now!</i>",
            reply_markup=board,
        )

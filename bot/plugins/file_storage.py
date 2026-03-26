import uuid, time, asyncio, requests
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot.client import app
from bot.database import files_col
from bot.utils.qr_generator import make_qr_bytes
from config import settings
from bot.utils.telegram_api import TelegramAPI

@app.on_message(filters.media & filters.private & filters.incoming)
async def handle_file(client: Client, message: Message):
    code = str(uuid.uuid4())
    sent = await TelegramAPI().copy_message(
        chat_id=settings.STORAGE_CHANNEL_ID,
        from_chat_id=message.chat.id,
        message_id=message.id,
    )
    if not sent:
        await message.reply_text(
            "❌ Failed to store the file. Please try again later."
        )
        return
    await files_col.insert_one(
        {
            "uuid": code,
            "file_msg_id": sent,
            "user_id": message.from_user.id,
            "file_type": "file",
            "timestamp": time.time(),
        }
    )
    apper = await client.get_me()
    link = f"https://t.me/{apper.username}?start={code}"
    try:
        def shorten_url():
            return requests.get(
                f"https://shrinkearn.com/api?api=9178c57f51d3630419b582621853e7c0713e439b&url={link}",
                timeout=8,
            ).json()["shortenedUrl"]

        link2 = await asyncio.to_thread(shorten_url)
    except Exception:
        link2 = link
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔗 Share File", url=f"https://t.me/share/url?url={link}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔗 Share File (secured)", url=f"https://t.me/share/url?url={link2}"
                )
            ],
        ]
    )
    qr_png = make_qr_bytes(link)
    await message.reply_photo(
        photo=qr_png,
        caption=f"✅ Stored!🔗\n\nLink-1: {link}\nLink-2 (secured): {link2}\n\nFILE_UUID: `{code}`",
        reply_to_message_id=message.id,
        reply_markup=keyboard,
    )

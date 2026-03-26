from pyrogram import filters
from pyrogram.types import Message
from bot.client import app


@app.on_message(
    filters.private
    & filters.text
    & ~filters.command(["start", "help", "list", "delete", "stats", "broad"])
)
async def unknown(_, message: Message):
    await message.reply(
        "<b>❓ Unknown command!</b>\n\n"
        "<i>I didn't recognize that command.\n"
        "Use /help to see all available commands.</i>",
    )

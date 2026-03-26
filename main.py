import asyncio

# Pyrogram's sync wrapper expects a current event loop at import time.
# Python 3.14 no longer creates one implicitly for the main thread.
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import idle
from bot.client import app as client


async def main():
    # Web app lifecycle is managed in Bot.on_startup/on_shutdown.
    # Starting it again here binds the same HOST/PORT twice and crashes startup.
    await client.start()
    await idle()
    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())

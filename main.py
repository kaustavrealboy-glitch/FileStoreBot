import asyncio
import os

# Pyrogram's sync wrapper expects a current event loop at import time.
# Python 3.14 no longer creates one implicitly for the main thread.
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import idle
from bot.client import app as client, create_web_app, start_webapp, stop_webapp


async def main():
    bot = client
    app = create_web_app()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    runner = await start_webapp(app, host, port)
    await bot.start()
    await idle()
    await stop_webapp(runner)
    await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())

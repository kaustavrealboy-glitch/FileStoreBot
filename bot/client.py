import asyncio

# Pyrogram's sync wrapper expects a current event loop at import time.
# Python 3.14 no longer creates one implicitly for the main thread.
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
from config import settings
from aiohttp import web
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


class Bot(Client):
    def __init__(self):
        super().__init__(
            "filebot",
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            bot_token=settings.BOT_TOKEN,
            workdir="bot/",
        )
        self.web_runner: web.AppRunner | None = None

    async def on_startup(self) -> None:
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        logger.info(f"{me.first_name} ✅")

        appc = create_web_app()
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8080"))
        self.web_runner = await start_webapp(appc, host, port)

    async def on_shutdown(self) -> None:
        if self.web_runner:
            await stop_webapp(self.web_runner)
        logger.info("Bot stopped")


app = Bot()


async def handle_root(request: web.Request) -> web.Response:
    return web.json_response({"developed by": "@Private_Bots"})


def create_web_app() -> web.Application:
    appz = web.Application(client_max_size=30 * 1024 * 1024)
    appz.router.add_get("/", handle_root)
    return appz


async def start_webapp(appx: web.Application, host: str, port: int) -> web.AppRunner:
    runner = web.AppRunner(appx)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info(f"Web server running on http://{host}:{port}")
    return runner


async def stop_webapp(runner: web.AppRunner) -> None:
    await runner.cleanup()
    logger.info("Web server shut down")


import pkgutil, os
import importlib

plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
for _, module_name, _ in pkgutil.iter_modules([plugins_dir]):
    importlib.import_module(f"bot.plugins.{module_name}")

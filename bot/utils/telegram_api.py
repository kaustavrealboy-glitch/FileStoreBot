from aiohttp import ClientSession, ClientTimeout
from config import settings


class TelegramAPI:
    def __init__(self):
        self.api = f"https://api.telegram.org/bot{settings.BOT_TOKEN}"

    async def copy_message(self, chat_id, from_chat_id, message_id):
        url = f"{self.api}/copyMessage"
        data = {
            "chat_id": int(chat_id),
            "from_chat_id": int(from_chat_id),
            "message_id": int(message_id),
        }
        timeout = ClientTimeout(total=10)
        try:
            async with ClientSession(timeout=timeout) as session:
                async with session.post(url, data=data) as response:
                    if response.status != 200:
                        return None
                    payload = await response.json()
                    return payload.get("result", {}).get("message_id")
        except Exception:
            return None

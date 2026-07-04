import os
import asyncio
from typing import Callable, Awaitable, Any

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers.route import router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN") or ""

# Two separate env vars — leave SECOND_TELEGRAM_ID empty/unset if there's
# only one user.
MY_ID = int(os.getenv("MY_TELEGRAM_ID") or "0")
SECOND_ID_RAW = os.getenv("SECOND_TELEGRAM_ID") or ""
ALLOWED_IDS = {MY_ID}
if SECOND_ID_RAW.strip():
    ALLOWED_IDS.add(int(SECOND_ID_RAW))


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict
    ) -> Any:
        user = data.get("event_from_user")
        if user and user.id not in ALLOWED_IDS:
            return
        return await handler(event, data)


dp = Dispatcher(storage=MemoryStorage())
dp.update.middleware(AccessMiddleware())
dp.include_router(router)


async def main():
    if MY_ID == 0:
        print("Warning: MY_TELEGRAM_ID is not set — no one will be able to use the bot.")
    bot = Bot(token=TOKEN)
    print("Start...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
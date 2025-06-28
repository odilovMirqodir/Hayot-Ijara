import asyncio
import logging
import sys
from aiogram import Dispatcher
from routers.message import message_router
from commands.commands import set_commands
from bot.loader.loader import bot

dp = Dispatcher()


async def main() -> None:
    await set_commands(bot)
    dp.include_router(message_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

import asyncio
import sqlite3

from config.config import Config, load_config
from aiogram import Bot, Dispatcher
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu

async def main():
    config = load_config()
    bot = Bot(
        token = config.tg_bot.token,
        parse_mode= "HTML"
        )
    dp = Dispatcher()

    await set_main_menu(bot= bot)
    
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates= True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
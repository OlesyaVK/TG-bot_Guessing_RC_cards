import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from dotenv import load_dotenv
from TG-bot_Guessing_RC_cards.handlers import register_handlers

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)

async def on_startup():
    register_handlers(dp)
    logging.info("Бот запущен")

async def main():
    await on_startup()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

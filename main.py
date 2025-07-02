import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from dotenv import load_dotenv

# Импорты обработчиков
from commands import register_commands
from callbacks import register_callbacks
from game import register_game_handlers

load_dotenv()

async def main():
    # Инициализация бота и диспетчера внутри async функции
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
    )

    # Регистрация обработчиков
    register_commands(dp)
    register_callbacks(dp)
    register_game_handlers(dp)

    logging.info("Бот запущен")
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

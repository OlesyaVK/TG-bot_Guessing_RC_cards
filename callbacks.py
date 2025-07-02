from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states import GameStates
from keyboards import get_names_keyboard

async def process_card(callback: CallbackQuery, state: FSMContext):
    card_type = callback.data.split("_")[1]
    await state.update_data(card_type=card_type)
    await callback.message.edit_text(f"Выбрана карта: {card_type}. Введите количество попыток (1-10):")
    await state.set_state(GameStates.waiting_for_attempts)

async def process_attempts(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
        await message.answer("Пожалуйста, введите число от 1 до 10")
        return

    data = await state.get_data()
    await state.update_data(attempts=int(message.text))
    await message.answer(
        "Теперь выберите ПРАВИЛЬНЫЙ ОТВЕТ:",
        reply_markup=get_names_keyboard(data['card_type'], [])
    )
    await state.set_state(GameStates.waiting_for_answer)

def register_callbacks(dp):
    dp.callback_query.register(process_card, F.data.startswith("card_"))
    dp.message.register(process_attempts, GameStates.waiting_for_attempts)

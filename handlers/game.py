from aiogram import Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import GameStates
from keyboards import get_names_keyboard, get_end_game_keyboard
from data.cards import CARDS_DATA

active_games: dict[int, dict] = {}

async def handle_correct_answer(callback: CallbackQuery, state: FSMContext, bot: Bot):
    correct_answer = callback.data.split("_")[1]
    data = await state.get_data()

    active_games[callback.message.chat.id] = {
        'creator_id': callback.from_user.id,
        'card_type': data['card_type'],
        'correct_answer': correct_answer,
        'used_names': [],
        'players': [],
        'attempts_left': data['attempts']
    }

    await callback.message.edit_text(
        f"🎮 Игра началась!\n"
        f"Карта: {data['card_type']}\n"
        f"Попыток: {data['attempts']}\n\n"
        f"Участники, пишите /join чтобы присоединиться!",
        reply_markup=get_end_game_keyboard()
    )
    await state.set_state(GameStates.game_in_progress)

async def handle_guess(callback: CallbackQuery, bot: Bot):
    chat_id = callback.message.chat.id
    if chat_id not in active_games:
        return

    game = active_games[chat_id]
    guessed_name = callback.data.split("_")[1]
    game['used_names'].append(guessed_name)
    game['attempts_left'] -= 1

    if guessed_name == game['correct_answer']:
        await callback.message.edit_text(
            f"🎉 Победа! {callback.from_user.full_name} угадал имя: {game['correct_answer']}"
        )
        del active_games[chat_id]
        return

    if game['attempts_left'] <= 0:
        await callback.message.edit_text("❌ Попытки закончились! Игра завершена.")
        del active_games[chat_id]
        return

    game['players'].append(game['players'].pop(0))
    await start_player_turn(chat_id, game['players'][0], bot)

async def start_player_turn(chat_id: int, player_id: int, bot: Bot):
    game = active_games[chat_id]
    player = await bot.get_chat_member(chat_id, player_id)
    await bot.send_message(
        chat_id,
        f"🎯 Ход игрока {player.user.full_name}. Выберите имя:",
        reply_markup=get_names_keyboard(game['card_type'], game['used_names'])
    )

async def end_game(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    if chat_id not in active_games:
        return

    game = active_games[chat_id]
    if callback.from_user.id != game['creator_id']:
        await callback.answer("Только создатель игры может её завершить!", show_alert=True)
        return

    await callback.message.edit_text(
        f"🛑 Игра завершена создателем.\nПравильный ответ: {game['correct_answer']}"
    )
    del active_games[chat_id]

def register_handlers(dp):
    dp.callback_query.register(handle_correct_answer, F.data.startswith("guess_"), GameStates.waiting_for_answer)
    dp.callback_query.register(handle_guess, F.data.startswith("guess_"))
    dp.callback_query.register(end_game, F.data == "end_game")
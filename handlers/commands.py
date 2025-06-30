from aiogram import F, types
from aiogram.fsm.context import FSMContext
from states import GameStates
from keyboards import get_cards_keyboard


async def cmd_start(message: types.Message, state: FSMContext):
    if message.chat.type not in ["group", "supergroup"]:
        await message.answer("Эта команда работает только в группах!")
        return

    await message.answer(
        "Админ, выберите тип карты для игры:",
        reply_markup=get_cards_keyboard()
    )
    await state.set_state(GameStates.waiting_for_card)


async def cmd_join(message: types.Message):
    from handlers.game import active_games, start_player_turn

    if message.chat.id not in active_games:
        await message.answer("Сейчас нет активной игры!")
        return

    game = active_games[message.chat.id]
    if message.from_user.id in game['players']:
        await message.answer("Вы уже в игре!")
        return

    game['players'].append(message.from_user.id)
    await message.answer(f"✅ {message.from_user.full_name} присоединился к игре!")

    if len(game['players']) == 1:
        await start_player_turn(message.chat.id, game['players'][0], message.bot)


def register_handlers(dp):
    dp.message.register(cmd_start, F.text == '/start')
    dp.message.register(cmd_join, F.text == '/join')
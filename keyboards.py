from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_cards_keyboard():
    builder = InlineKeyboardBuilder()
    for card in CARDS_DATA.keys():
        builder.button(text=card, callback_data=f"card_{card}")
    builder.adjust(1)
    return builder.as_markup()

def get_names_keyboard(card_type: str, used_names: list):
    builder = InlineKeyboardBuilder()
    for name in CARDS_DATA[card_type]:
        if name not in used_names:
            builder.button(text=name, callback_data=f"guess_{name}")
    builder.adjust(2)
    return builder.as_markup()

def get_end_game_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Завершить игру", callback_data="end_game")
    return builder.as_markup()

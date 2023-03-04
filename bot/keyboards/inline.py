from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.lexicon import RU_LEXICON

agree_button = InlineKeyboardMarkup(inline_keyboard=(
    [[InlineKeyboardButton(text=RU_LEXICON['agree_button'], callback_data='agree')]]
    ))
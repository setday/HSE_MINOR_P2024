from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .entry_router_text import text_take_the_servey, text_update

def get_entry_servey_suggestion_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=text_take_the_servey,
        callback_data='take_the_servey')
    )
    return builder.as_markup()

def get_update_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=text_update,
        callback_data='update')
    )
    return builder.as_markup()

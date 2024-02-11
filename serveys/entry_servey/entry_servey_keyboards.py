from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .entry_servey_text import frequency_answers, text_lets_go

def get_first_question_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, value in frequency_answers.items():
        builder.add(InlineKeyboardButton(text=key, callback_data=value))
    builder.adjust(1)

    return builder.as_markup()

def get_second_question_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(1, 11):
        builder.add(InlineKeyboardButton(
            text=f'{i}',
            callback_data=f'{i}'
        ))
    builder.adjust(5)

    return builder.as_markup()

def get_entry_servey_continuation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=text_lets_go,
        callback_data='start_weekly_servey'
    ))
    return builder.as_markup()

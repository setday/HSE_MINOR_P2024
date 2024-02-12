from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from filters.admin_chat_filter import AdminChatFilter

import serveys.servey_manager as servey_manager

from .back_chat_utils import send_data_to_back
from data_register import data_register as dr

router = Router()

@router.message(
        AdminChatFilter(False),
)
async def echo_handler(message: Message) -> None:
    await send_data_to_back(message.bot, f'Новое сообщение от пользователя {message.from_user.id}:\n{str(message.text)}')
    # await message.reply(message.text)
    await message.reply('Зафиксировал.')

@router.message(
        AdminChatFilter(True),
        Command(commands=['send_stat', 'ss']),
)
async def feedback_handler(
        message: Message,
        command: CommandObject
) -> None:
    if command.args is None:
        await message.reply(
            "Ошибка: не переданы аргументы"
        )
        return

    try:
        cmd, user_id, text_to_send = message.html_text.split(" ", maxsplit=2)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/send_stat <user_id> <stat>",
            parse_mode=None
        )
        return
    if user_id == 'all':
        user_id = dr.get_all_users()
    else:
        user_id = [int(user_id)]
        
    for user in user_id:
        await send_data_to_back(message.bot, f'Отправка статистики пользователю {user}:\n{text_to_send}')
        if message.photo:
            await message.bot.send_photo(user, message.photo[-1].file_id, caption=text_to_send)
        else:
            await message.bot.send_message(user, text_to_send, parse_mode="HTML")

@router.message(
        AdminChatFilter(True),
        Command(commands=['start_daily_servey', 'sds']),
)
async def start_daily_servey_handler(
        message: Message,
        state: FSMContext
) -> None:
    if not message.bot:
        return

    await servey_manager.sds_for_all(message.bot, state.storage)

@router.message(
        AdminChatFilter(True),
        Command(commands=['start_weekly_servey', 'sws']),
)
async def start_weekly_servey_handler(
        message: Message,
        state: FSMContext
) -> None:
    if not message.bot:
        return

    await servey_manager.sws_for_all(message.bot, state.storage)

@router.message(
        AdminChatFilter(True),
        Command(commands=['stop_timer', 'st']),
)
async def stop_timer_handler(
        message: Message,
        state: FSMContext
) -> None:
    if not message.bot:
        return
    
    servey_manager.is_timer_working = False
    
    await message.reply('Таймер остановлен.')

@router.message(
        AdminChatFilter(True),
        Command(commands=['cmd']),
)
async def execute_command_handler(
        message: Message,
        state: FSMContext
) -> None:
    if not message.bot:
        return
    
    await message.reply('Команда НЕ выполнена.')

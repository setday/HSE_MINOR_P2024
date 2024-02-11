from email import message
from aiogram.types import Message
from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandObject

from filters.admin_chat_filter import AdminChatFilter, back_chat_id

router = Router()

async def send_data_to_back(bot: Bot, data: str) -> int:
    message = await bot.send_message(back_chat_id, text=data)
    
    return message.message_id

async def update_data_to_back(bot: Bot, message_id: int, data: str) -> None:
    await bot.edit_message_text(chat_id=back_chat_id, message_id=message_id, text=data)

@router.message(
        AdminChatFilter(False),
)
async def echo_handler(message: Message) -> None:
    await send_data_to_back(message.bot, f'Новое сообщение от пользователя {message.from_user.id}:\n{str(message.text)}')
    # await message.reply(message.text)
    await message.answer('Зафиксировал.')

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
        user_id, text_to_send = command.args.split(" ", maxsplit=1)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/send_stat <user_id> <stat>",
            parse_mode=None
        )
        return
    message.text = text_to_send
    await message.copy_to(back_chat_id)

from aiogram import Bot
from filters.admin_chat_filter import back_chat_id

async def send_data_to_back(bot: Bot, data: str) -> int:
    message = await bot.send_message(back_chat_id, text=data)
    
    return message.message_id

async def update_data_to_back(bot: Bot, message_id: int, data: str) -> None:
    await bot.edit_message_text(chat_id=back_chat_id, message_id=message_id, text=data)


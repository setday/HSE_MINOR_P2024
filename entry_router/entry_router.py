from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart

from filters.admin_chat_filter import AdminChatFilter

from .entry_router_keyboards import *
from .entry_router_text import *

class EntryRouter(Router):
    def __init__(self) -> None:
        super().__init__()

        self.message.register(self.send_welcome, CommandStart(), AdminChatFilter(False))

    async def send_welcome(self, message: types.Message) -> None:
        print('New user:', message.from_user)

        await message.answer(text_hello_with_explanation)
        await message.answer(text_entry_servey_suggestion)

        await message.answer(text_entry_servey_continuation_suggestion, reply_markup=get_entry_servey_suggestion_keyboard())

router = EntryRouter()

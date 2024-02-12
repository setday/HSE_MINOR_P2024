from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart, Command

from filters.admin_chat_filter import AdminChatFilter
from filters.register_filter import RegisterFilter

from .entry_router_keyboards import *
from .entry_router_text import *

from data_register import data_register as dr

class EntryRouter(Router):
    def __init__(self) -> None:
        super().__init__()

        self.message.register(self.send_welcome, CommandStart(), AdminChatFilter(False), RegisterFilter(False))
        self.message.register(self.already_register, CommandStart(), AdminChatFilter(False), RegisterFilter(True))
        self.message.register(self.stop_subscription, Command('stop'), AdminChatFilter(False))

    async def send_welcome(self, message: types.Message) -> None:
        print('New user:', message.from_user, message.chat.id)

        await message.answer(text_hello_with_explanation)
        await message.answer(text_entry_servey_suggestion)

        dr.register_data(message.from_user.id, True, 'reg')

        await message.answer(text_entry_servey_continuation_suggestion, reply_markup=get_entry_servey_suggestion_keyboard())

    async def already_register(self, message: types.Message) -> None:
        await message.answer('Ты уже начал общение.')

    async def stop_subscription(self, message: types.Message) -> None:
        if not message.from_user:
            return

        dr.get_data(message.from_user.id)['info']['subscribe'] = False
        dr.get_data(message.from_user.id)['reg'] = False

        await message.answer(text_subscription_stopped)

router = EntryRouter()

from datetime import time
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from console.command_handler import CommandHandler

from filters.admin_chat_filter import AdminChatFilter

import serveys.servey_manager as servey_manager

from .back_chat_utils import send_data_to_back
from utils.data_register import DataRegister

class BackChatRouter(Router):
    def __init__(self, bot: Bot, dr: DataRegister, ch: CommandHandler, timer: servey_manager.TimerServey) -> None:
        super().__init__()

        self.bot = bot
        self.dr = dr
        self.ch = ch
        self.timer = timer

        self.message.register(self.echo_handler, AdminChatFilter(False))
        self.message.register(self.feedback_handler, AdminChatFilter(True), Command(commands=['send_stat', 'ss']))
        self.message.register(self.start_daily_servey_handler, AdminChatFilter(True), Command(commands=['start_daily_servey', 'sds']))
        self.message.register(self.start_weekly_servey_handler, AdminChatFilter(True), Command(commands=['start_weekly_servey', 'sws']))
        self.message.register(self.stop_timer_handler, AdminChatFilter(True), Command(commands=['stop_timer', 'st']))
        self.message.register(self.start_timer_handler, AdminChatFilter(True), Command(commands=['continue_timer', 'ct']))
        self.message.register(self.add_servey_handler, AdminChatFilter(True), Command(commands=['add_servey', 'as']))
        self.message.register(self.remove_servey_handler, AdminChatFilter(True), Command(commands=['remove_servey', 'rs']))
        self.message.register(self.execute_command_handler, AdminChatFilter(True), Command(commands=['cmd']))
        
    async def echo_handler(self, message: Message) -> None:
        await send_data_to_back(self.bot, f'Новое сообщение от пользователя {message.from_user.id}:\n{str(message.text)}')
        # await message.reply(message.text)
        await message.reply('Зафиксировал.')

    async def feedback_handler(
            self, 
            message: Message,
            command: CommandObject
    ) -> None:
        if command.args is None:
            await message.reply(
                "Ошибка: не переданы аргументы"
            )
            return

        try:
            _, user_id, text_to_send = message.html_text.split(" ", maxsplit=2)
        except ValueError:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/send_stat <user_id> <stat>",
                parse_mode=None
            )
            return
        if user_id == 'all':
            user_id = self.dr.get_all_users()
        else:
            user_id = [int(user_id)]
            
        for user in user_id:
            await send_data_to_back(self.bot, f'Отправка статистики пользователю {user}:\n{text_to_send}')
            if message.photo:
                await self.bot.send_photo(user, message.photo[-1].file_id, caption=text_to_send)
            else:
                await self.bot.send_message(user, text_to_send, parse_mode="HTML")

    async def start_daily_servey_handler(
            self, 
            message: Message,
            state: FSMContext
    ) -> None:
        await servey_manager.sds_for_all(self.bot, state.storage)

    async def start_weekly_servey_handler(
            self, 
            message: Message,
            state: FSMContext
    ) -> None:
        await servey_manager.sws_for_all(self.bot, state.storage)

    async def stop_timer_handler(
            self, 
            message: Message
    ) -> None:
        servey_manager.is_timer_working = False
        
        await message.reply('Таймер остановлен.')

    async def start_timer_handler(
            self, 
            message: Message
    ) -> None:
        servey_manager.is_timer_working = True
        
        await message.reply('Таймер запущен.')

    async def add_servey_handler(
            self, 
            message: Message,
            command: CommandObject
    ) -> None:
        if command.args is None:
            await message.reply(
                "Ошибка: не переданы аргументы"
            )
            return

        try:
            t, servey_type = command.args.split(" ", maxsplit=1)
            t_h, t_m = t.split(":")
            t_n = time(hour=int(t_h), minute=int(t_m))
        except ValueError:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/add_servey <servey_time> <servey_type>",
                parse_mode=None
            )

        if servey_type == 'daily' or servey_type == 'd':
            await self.timer.add_servey(1, t_n)
        elif servey_type == 'weekly' or servey_type == 'w':
            await self.timer.add_servey(2, t_n)
        else:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/add_servey 18:00 daily",
                parse_mode=None
            )

    async def remove_servey_handler(
            self, 
            message: Message,
            command: CommandObject
    ) -> None:
        if command.args is None:
            await message.reply(
                "Ошибка: не переданы аргументы"
            )
            return

        try:
            servey_id = int(command.args)
        except ValueError:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/remove_servey <servey_id>",
                parse_mode=None
            )

        await self.timer.remove_servey(servey_id - 1)

    async def execute_command_handler(
            self, 
            message: Message,
            command: CommandObject
    ) -> None:
        if command.args is None:
            await message.reply(
                "Ошибка: не переданы аргументы"
            )
            return

        await self.ch.handle_command(command.args)

        await message.reply('Команда выполнена.')

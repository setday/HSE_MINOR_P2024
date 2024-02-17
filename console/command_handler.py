import asyncio
import sys

from aiogram import Bot, Dispatcher

from utils.data_register import DataRegister
import serveys.servey_manager as servey_manager

from entry_router.entry_router_text import text_update_is_there
from entry_router.entry_router_keyboards import get_update_keyboard

class CommandHandler:
    def __init__(self, bot: Bot, dp: Dispatcher, dr: DataRegister) -> None:
        self.bot = bot
        self.dp = dp
        self.dr = dr

    async def handle_command(self, command: str) -> None:
        command = command.split()[0]
        print('->', command)
        if command == 'exit':
            await self.handle_command('save')
            print('Exiting...')
            sys.exit(0)

        if command == 'save':
            print('Saving...')
            self.dr.save_dictionary()
            return
        
        if command == 'load':
            print('Loading...')
            self.dr.load_dictionary()
            await self.handle_command('user_data')
        
        if command == 'user_data' or command == 'ud':
            print(self.dr._data_dictonary)
            return
        
        if command == 'start_daily_servey' or command == 'sds':
            await servey_manager.sds_for_all(self.bot, self.dp.storage)
            return
        
        if command == 'start_weekly_servey' or command == 'sws':
            await servey_manager.sws_for_all(self.bot, self.dp.storage)
            return
        
        if command == 'suggest_update' or command == 'su':
            for user_id in self.dr.get_all_users():
                # if dr.get_data(user_id)['reg']['subscribe']:
                await self.bot.send_message(user_id, text_update_is_there, reply_markup=get_update_keyboard())
            return
        
        if command == 'help':
            print('''
    Commands:
    1) exit - exit the program
    2) save - save the data
    3) user_data - print the user data
    4) start_daily_servey - start the daily servey
    5) start_weekly_servey - start the weekly servey
    6) suggest_update - suggest update to all users
    4) help - print this message
                ''')
            return
        
        print('Unknown command')

    async def run_command_loop(self) -> None:
        while True:
            cmd = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            await self.handle_command(cmd)

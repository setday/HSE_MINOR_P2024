import asyncio
import re
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

    async def handle_command(self, command: str) -> str:
        command = command.split()[0]
        res = f'-> {command}\n'
        
        if command == 'exit':
            await self.handle_command('save')
            res += 'Exiting...\n'
            print(res)
            sys.exit(0)

        if command == 'save':
            self.dr.save_dictionary()
            res += 'Saved.\n'
            return res
        
        if command == 'load':
            self.dr.load_dictionary()
            res += 'Loaded.\n'
            await self.handle_command('user_data')

            return res
        
        if command == 'user_data' or command == 'ud':
            res += f'User data:\n{self.dr._data_dictonary}\n'
            return res
        
        if command == 'start_daily_servey' or command == 'sds':
            await servey_manager.sds_for_all(self.bot, self.dp.storage)
            res += 'Daily servey started for all users.\n'
            return res
        
        if command == 'start_weekly_servey' or command == 'sws':
            await servey_manager.sws_for_all(self.bot, self.dp.storage)
            res += 'Weekly servey started for all users.\n'
            return res
        
        if command == 'suggest_update' or command == 'su':
            for user_id in self.dr.get_user_list():
                if self.dr.get_user_info(user_id).get('subscribe', True):
                    await self.bot.send_message(user_id, text_update_is_there, reply_markup=get_update_keyboard())
            res += 'Suggested update to all users.\n'
            return res
        
        if command == 'stop_timer' or command == 'st':
            servey_manager.is_timer_working = False
            
            res += 'Timer stopped.\n'
            return res
        
        if command == 'continue_timer' or command == 'ct':
            servey_manager.is_timer_working = True
            
            res += 'Timer started.\n'
            return res
        
        if command == 'help':
            res += '''
    Commands:
    1) exit - exit the program
    2) save - save the data
    3) load - load the data
    4) user_data - print the user data
    5) start_daily_servey - start the daily servey
    6) start_weekly_servey - start the weekly servey
    7) suggest_update - suggest update to all users
    8) stop_timer - stop automatic servey sending
    9) continue_timer - continue automatic servey sending
    10) help - print this message
                '''
            return res
        
        res += 'Unknown command\n'
        return res

    async def run_command_loop(self) -> None:
        while True:
            cmd = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            print(await self.handle_command(cmd))

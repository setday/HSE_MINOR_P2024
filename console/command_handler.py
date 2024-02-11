import asyncio
import sys

from aiogram import Bot, Dispatcher

from data_register import DataRegister
import serveys.servey_manager as servey_manager

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
        
        if command == 'user_data':
            print(self.dr.data_dictonary)
            return
        
        if command == 'ds':
            for user_id in self.dr.data_dictonary:
                if self.dr.data_dictonary[user_id]['info']['subscribe']:
                    await servey_manager.sds(self.bot, user_id, self.dp.storage)
            return
        
        if command == 'ws':
            for user_id in self.dr.data_dictonary:
                if self.dr.data_dictonary[user_id]['info']['subscribe']:
                    await servey_manager.sws(self.bot, user_id, self.dp.storage)
            return
        
        if command == 'help':
            print('''
    Commands:
    1) exit - exit the program
    2) save - save the data
    3) user_data - print the user data
    4) help - print this message
                ''')
            return
        
        print('Unknown command')

    async def run_command_loop(self) -> None:
        while True:
            cmd = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            await self.handle_command(cmd)

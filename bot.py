import asyncio
import logging
from os import getenv

import serveys.entry_servey.entry_servey as entry_servey

from aiogram import Bot, Dispatcher, enums

from console.command_handler import CommandHandler
import serveys.servey_manager as servey_manager

import entry_router.entry_router as entry_router
import serveys.weekly_servey.weekly_servey as weekly_servey
import serveys.daily_servey.daily_servey as daily_servey
import back_chat.back_chat_router as back_chat

from utils.data_register import data_register as dr

# API_TOKEN = '6945025628:AAFjTcXORaH7HWM-1fBGBTrqMGpyWb7vQoA' # Test
API_TOKEN = '6812122141:AAGE17rpSpxlbH4F-aa7R1P9TSLD9-JM3_o' # Prod

bot = Bot(API_TOKEN, parse_mode=enums.ParseMode.HTML)
dp = Dispatcher()
ch = CommandHandler(bot, dp, dr)

ts = servey_manager.TimerServey(bot, dp.storage)

entry_router_router = entry_router.EntryRouter(bot)

weekly_servey_router = weekly_servey.WeeklyServeyRouter(bot)
daily_servey_router = daily_servey.DailyServeyRouter(bot)
back_chat_router = back_chat.BackChatRouter(bot, dr, ch, ts)

async def saver() -> None:
    while True:
        await ch.handle_command('save')

        await asyncio.sleep(60 * 60 * 6)

async def main() -> None:
    dp.include_routers(
        entry_router_router,
        servey_manager.router,
        entry_servey.router,
        daily_servey_router,
        weekly_servey_router,
        back_chat_router
        )

    # await bot.delete_webhook(drop_pending_updates=True)

    await ch.handle_command('load')
    cmds = asyncio.create_task(ch.run_command_loop())
    poll = asyncio.create_task(dp.start_polling(bot))
    save = asyncio.create_task(saver())
    tstk = asyncio.create_task(ts.start())

    print('Bot started')

    await poll
    await tstk
    await cmds
    await save

if __name__ == "__main__":
    print('Initializing...')
    asyncio.run(main())

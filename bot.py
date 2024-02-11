import asyncio
import logging
from os import getenv

import serveys.entry_servey.entry_servey as entry_servey

from aiogram import Bot, Dispatcher, enums

from console.command_handler import CommandHandler
import back_chat
import serveys.servey_manager as servey_manager

import entry_router.entry_router as entry_router
import serveys.weekly_servey.weekly_servey as weekly_servey
import serveys.daily_servey.daily_servey as daily_servey

from data_register import data_register as dr

API_TOKEN = '6812122141:AAGE17rpSpxlbH4F-aa7R1P9TSLD9-JM3_o'

bot = Bot(API_TOKEN, parse_mode=enums.ParseMode.HTML)
dp = Dispatcher()
ch = CommandHandler(bot, dp, dr)

weekly_servey_router = weekly_servey.WeeklyServeyRouter(bot)
daily_servey_router = daily_servey.DailyServeyRouter(bot)

async def main() -> None:
    dp.include_routers(
        entry_router.router,
        servey_manager.router,
        entry_servey.router,
        daily_servey_router,
        weekly_servey_router,
        back_chat.router
        )

    await bot.delete_webhook(drop_pending_updates=True)

    cmds = asyncio.create_task(ch.run_command_loop())
    poll = asyncio.create_task(dp.start_polling(bot))

    print('Bot started')

    await poll
    await cmds

if __name__ == "__main__":
    # logging.basicConfig(
        # level=logging.INFO,
        # format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    # )
    print('Initializing...')
    asyncio.run(main())

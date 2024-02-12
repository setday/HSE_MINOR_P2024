import asyncio
import random
from datetime import datetime, time
from venv import logger

from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.storage.base import BaseStorage

from data_register import data_register as dr
from back_chat.back_chat_utils import send_data_to_back

from service_text import text_error_try_again
from .weekly_servey.weekly_servey import interupt_weekly_servey, start_weekly_servey
from .daily_servey.daily_servey import interupt_daily_servey, start_daily_servey

router = Router()

@router.callback_query(F.data == 'start_weekly_servey')
async def weekly_dservey_start(callback: CallbackQuery, state: FSMContext) -> None:
    if not callback.bot:
        callback.answer(text_error_try_again)

        return

    # await callback.answer('Подписка оформлена! Стоимость подписки: 10 рублей в день (списание производится по номеру телефона).')
    await callback.answer('Ежедневные анкеты включены!')
    await callback.bot.send_message(callback.from_user.id, 'Пожалуйста, включи уведомления. Я буду отправлять сообщения в разное время. Скоро тебе начнут приходить краткие опросы о твоем состоянии. В качестве ответа тебе нужно будет либо нажать на кнопку, либо ввести несколько слов.\n(Если ты захочешь остановить опросы, напиши /stop)')

    # logger.info(f'Weekly servey for user {callback.from_user.id} started.')
    
    # await wait_next_servey(callback.bot, callback.from_user.id, state.storage)

async def sds(bot: Bot, user_id: int, storage: BaseStorage) -> None:
    await interupt_daily_servey(bot, user_id, storage)
    await start_daily_servey(bot, user_id, storage)

async def sws(bot: Bot, user_id: int, storage: BaseStorage) -> None:
    await interupt_weekly_servey(bot, user_id, storage)
    await start_weekly_servey(bot, user_id, storage)
    
async def sds_for_all(bot: Bot, storage: BaseStorage) -> None:
    for user_id in dr.get_all_users():
        if dr.get_data(user_id)['info']['subscribe']:
            await sds(bot, user_id, storage)

    await send_data_to_back(bot, 'Начат ежедневный опрос для всех подписчиков.')

async def sws_for_all(bot: Bot, storage: BaseStorage) -> None:
    for user_id in dr.get_all_users():
        if dr.get_data(user_id)['info']['subscribe']:
            await sws(bot, user_id, storage)

    await send_data_to_back(bot, 'Начат еженедельный опрос для всех подписчиков.')

async def wait_next_servey(bot: Bot, user_id: int, storage: BaseStorage) -> None:
    # user_data = dr.get_data(user_id)
    # last_servey = user_data['servey'][-1]
    # last_servey_date = last_servey['date']
    # current_date = time.time()

    # if current_date - last_servey_date > 604800:
        # return True
    # return False

    # while True:
        await asyncio.sleep(2)
        await sds(bot, user_id, storage)

        await asyncio.sleep(10)
        await sws(bot, user_id, storage)

is_timer_working = True

class TimerServey:
    def __init__(self, bot: Bot, storage: BaseStorage) -> None:
        self.bot = bot
        self.storage = storage

    async def start(self) -> None:
        while is_timer_working:
            await self.start_servey()

            await asyncio.sleep(60 * 60 * 2)

    async def start_servey(self) -> None:
        servey_type = self.check_if_servey()

        if servey_type == 0:
            print(f'Servey start failed. No servey for now.')

            return
        
        await self.wait_next_servey(servey_type)

        if servey_type == 1 and is_timer_working:
            await sds_for_all(self.bot, self.storage)
        if servey_type == 2 and is_timer_working:
            await sws_for_all(self.bot, self.storage)

        await asyncio.sleep(60 * 60 * 4)

    async def wait_next_servey(self, servey_type: int) -> None:
        delta = 0

        if servey_type == 1:
            delta = int(60 * 60 * 3 * random.random())
        if servey_type == 2:
            hour = datetime.now().hour
            delta = 60 * 60 * (20 - hour)

        print(f'Expected servey in {delta} seconds. Type: {servey_type}')

        await asyncio.sleep(delta)

    def check_if_servey(self) -> int: # 0 - no servey, 1 - daily servey, 2 - weekly servey
        date = datetime.now()
        servey_type = 1

        if date.isoweekday() == 7:
            servey_type = 2

        t = date.time()
        if t >= time(12, 00) and t <= time(17, 00):
            return servey_type
        if t >= time(17, 00) and t <= time(22, 00):
            return servey_type
        return 0

import asyncio
import random
from datetime import time
from turtle import update
from venv import logger

from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.storage.base import BaseStorage

from utils.data_register import data_register as dr
from back_chat.back_chat_utils import send_data_to_back

from utils.service_text import text_error_try_again
from .weekly_servey.weekly_servey import interupt_weekly_servey, start_weekly_servey
from .daily_servey.daily_servey import interupt_daily_servey, start_daily_servey

import utils.timer as timer

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

        self.servey_queue: list[tuple[time, int]] = []

    async def print_servey_queue(self) -> None:
        txt = 'Текущая очередь опросов:\n'
        for i in range(len(self.servey_queue)):
            txt += f'{i + 1}) {self.servey_queue[i][0]} - {self.servey_queue[i][1]}\n'
        await send_data_to_back(self.bot, txt)

    async def add_servey(self, servey_type: int, t: time) -> None:
        self.servey_queue.append((t, servey_type))
        self.servey_queue.sort()
        await self.print_servey_queue()

    async def remove_servey(self, id: int) -> None:
        self.servey_queue.pop(id)
        await self.print_servey_queue()

    async def update_servey_queue(self) -> None:
        t = timer.get_time()

        while len(self.servey_queue) > 0 and self.servey_queue[0][0] < t:
            self.servey_queue.pop(0)

        if len(self.servey_queue) == 0:
            if timer.get_weekday() != 5:
                if t < time(12, 00):
                    self.servey_queue.append((
                        timer.add_time(
                            time(12, 00),
                            int(60 * 60 * 4 * random.random())
                        ), 1
                    ))
                if t < time(18, 0):
                    self.servey_queue.append((
                        timer.add_time(
                            time(18, 0),
                            int(60 * 60 * 4 * random.random())
                        ), 1
                    ))
            else:
                if t < time(20, 0):
                    self.servey_queue.append((
                        timer.add_time(
                            time(16, 0),
                            int(60 * 60 * 4 * random.random())
                        ), 2
                    ))

        self.servey_queue.sort()
        await self.print_servey_queue()

    async def start(self) -> None:
        while True:
            await self.update_servey_queue()

            if len(self.servey_queue) == 0:
                await asyncio.sleep(
                    timer.get_time_to(time(10, 00))
                )
                continue
            
            await asyncio.sleep(
                timer.get_time_to(self.servey_queue[0][0]) + 10
            )
            if self.servey_queue[0][0] < timer.get_time():
                await self.start_servey(self.servey_queue[0][1])
            self.servey_queue.pop(0)

    async def start_servey(self, servey_type: int) -> None:
        if servey_type == 0 or is_timer_working == False:
            print(f'Servey start failed. No servey for now.')

            return
        
        if servey_type == 1:
            await sds_for_all(self.bot, self.storage)
        if servey_type == 2:
            await sws_for_all(self.bot, self.storage)

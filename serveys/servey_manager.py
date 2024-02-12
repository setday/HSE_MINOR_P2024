import asyncio
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
    await callback.answer('Подписка оформлена!')
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

async def sws_for_all(bot: Bot, storage: BaseStorage) -> None:
    for user_id in dr.get_all_users():
        if dr.get_data(user_id)['info']['subscribe']:
            await sws(bot, user_id, storage)

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

import utils.timer as timer

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.fsm.storage.base import StorageKey, BaseStorage

from utils.data_register import data_register as dr
from back_chat.back_chat_utils import send_data_to_back, update_data_to_back

from .weekly_servey_text import *

class OrderWeeklyServey(StatesGroup):
    writting_question_1 = State()
    writting_question_2 = State()

async def start_weekly_servey(bot: Bot, user_id: int, storage: BaseStorage) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                # InlineKeyboardButton(text=text_restart_servey, callback_data=text_restart_servey),
                InlineKeyboardButton(text=text_cancel_servey, callback_data=text_cancel_servey)
            ]
        ]
    )

    await bot.send_message(user_id, text=text_lets_begin_weekly_servey)
    await bot.send_message(user_id, text=text_question_1, reply_markup=keyboard)
    
    state = FSMContext(storage=storage, key=StorageKey(bot.id, user_id, user_id))

    await state.update_data(servey_type='weekly')
    await state.update_data(date=timer.get_date())
    await state.update_data(user_id=user_id)
    await state.update_data(user_name=dr.get_data(user_id)['info']['name'])
    await state.update_data(q1={
        'question_time': timer.get_time(),
        'question': text_question_1
    })
    user_data = await state.get_data()
    await state.update_data(message_id=await send_data_to_back(bot, format_user_data(user_data)))

    await state.set_state(OrderWeeklyServey.writting_question_1)

async def interupt_weekly_servey(bot: Bot, user_id: int, storage: BaseStorage) -> None:
    state = FSMContext(storage=storage, key=StorageKey(bot.id, user_id, user_id))

    if await state.get_state() is None:
        return

    await bot.send_message(user_id, text_weekly_servey_cancelled)
    
    await state.clear()

class WeeklyServeyRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.weekly_servey_restart, F.text == text_restart_servey)
        self.callback_query.register(self.weekly_servey_cancel, F.data == text_cancel_servey)

        self.message.register(self.question_handler_1, OrderWeeklyServey.writting_question_1)
        self.message.register(self.question_handler_2, OrderWeeklyServey.writting_question_2)

    async def weekly_servey_restart(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await start_weekly_servey(self.bot, message.chat.id, state.storage)

    async def weekly_servey_cancel(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.update_data(a1={
            'answer_time':  timer.get_time(),
            'answer': callback.data
        })
        
        await callback.answer(text_weekly_servey_cancelled)

        user_data = await state.get_data()
        await update_data_to_back(self.bot, user_data['message_id'], format_user_data(user_data))
        
        await interupt_weekly_servey(self.bot, callback.from_user.id, state.storage)

    async def question_handler_1(self, message: Message, state: FSMContext) -> None:
        await state.update_data(a1={
            'answer_time': timer.get_time(),
            'answer': message.text
        })

        await message.answer(text_question_2)

        await state.update_data(q2={
            'question_time': timer.get_time(),
            'question': text_question_2
        })
        user_data = await state.get_data()
        await update_data_to_back(self.bot, user_data['message_id'], format_user_data(user_data))
        await state.set_state(OrderWeeklyServey.writting_question_2)

    async def writing_strategies(self, message: Message, state: FSMContext) -> None:
        await state.update_data(strategies=message.text)

        await message.answer(text_question_3)

        await state.set_state(OrderWeeklyServey.writting_question_2)

    async def question_handler_2(self, message: Message, state: FSMContext) -> None:
        await state.update_data(a2={
            'answer_time': timer.get_time(),
            'answer': message.text
        })
        
        user_data = await state.get_data()
        # print('Server info: %s', user_data)
        dr.merge_data(user_data['user_id'], user_data, 'servey')
        await update_data_to_back(self.bot, user_data['message_id'], format_user_data(user_data))

        await message.answer(
            text=text_thanks_for_answers
        )

        await state.clear()

        # await wait_next_servey(message.bot, message.chat.id, state.storage)

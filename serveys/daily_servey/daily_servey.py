import utils.timer as timer

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.fsm.storage.base import StorageKey, BaseStorage

from utils.data_register import data_register as dr
from back_chat.back_chat_utils import send_data_to_back, update_data_to_back

from .daily_servey_text import *
from utils.service_text import text_no, text_yes

class OrderDailyServey(StatesGroup):
    writting_question_1 = State()
    writting_question_2 = State()
    writting_question_3 = State()
    writting_question_4 = State()
    writting_question_5 = State()

async def start_daily_servey(bot: Bot, user_id: int, storage: BaseStorage) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text_yes, callback_data=text_yes),
                InlineKeyboardButton(text=text_no, callback_data=text_no)
            ]
        ]
    )

    await bot.send_message(user_id, text=text_lets_begin_daily_servey)
    await bot.send_message(user_id, text=text_question[0], reply_markup=keyboard)
    
    state = FSMContext(storage=storage, key=StorageKey(bot.id, user_id, user_id))
    # print(storage, bot.id, user_id, state)

    await state.update_data(servey_type='daily')
    await state.update_data(date=timer.get_date())
    await state.update_data(user_id=user_id)
    await state.update_data(q1={
        'question_time': timer.get_time(),
        'question': text_question[0]
    })
    user_data = await state.get_data()
    await state.update_data(message_id=await send_data_to_back(bot, format_user_data(user_data)))

    await state.set_state(OrderDailyServey.writting_question_1)

async def interupt_daily_servey(bot: Bot, user_id: int, storage: BaseStorage) -> None:
    state = FSMContext(storage=storage, key=StorageKey(bot.id, user_id, user_id))

    if await state.get_state() is None:
        return

    await bot.send_message(user_id, text_daily_servey_cancelled)
    
    await state.clear()

class DailyServeyRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.message.register(self.daily_servey_restart, F.text == text_restart_servey)
        self.callback_query.register(self.daily_servey_cancel, F.data == text_no)

        self.callback_query.register(self.question_handler_1, OrderDailyServey.writting_question_1, F.data == text_yes)
        self.message.register(self.question_handler_2, OrderDailyServey.writting_question_2)
        self.message.register(self.question_handler_3, OrderDailyServey.writting_question_3)
        self.message.register(self.question_handler_4, OrderDailyServey.writting_question_4)
        self.message.register(self.question_handler_5, OrderDailyServey.writting_question_5)
        
    async def daily_servey_restart(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await start_daily_servey(self.bot, message.chat.id, state.storage)

    async def daily_servey_cancel(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.update_data(a1={
            'answer_time': timer.get_time(),
            'answer': callback.data
        })
        
        await callback.answer(text_daily_servey_cancelled)

        user_data = await state.get_data()
        await update_data_to_back(self.bot, user_data['message_id'], format_user_data(user_data))
        
        await interupt_daily_servey(self.bot, callback.from_user.id, state.storage)

    async def question_handler_1(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.update_data(a1={
            'answer_time': timer.get_time(),
            'answer': callback.data
        })

        await callback.answer('Начнём!')
        await self.bot.send_message(callback.from_user.id, text_question[1])

        await state.update_data(q2={
            'question_time': timer.get_time(),
            'question': text_question[1]
        })
        user_data = await state.get_data()
        await update_data_to_back(self.bot, user_data['message_id'], format_user_data(user_data))
        await state.set_state(OrderDailyServey.writting_question_2)

    async def question_handler_2(self, message: Message, state: FSMContext) -> None:
        await state.update_data(a2={
            'answer_time': timer.get_time(),
            'answer': message.text
        })

        await message.answer(text_question[2])

        await state.update_data(q3={
            'question_time': timer.get_time(),
            'question': text_question[2]
        })
        user_data = await state.get_data()
        await update_data_to_back(self.bot, user_data['message_id'], format_user_data(user_data))
        await state.set_state(OrderDailyServey.writting_question_3)

    async def question_handler_3(self, message: Message, state: FSMContext) -> None:
        await state.update_data(a3={
            'answer_time': timer.get_time(),
            'answer': message.text
        })

        await message.answer(text_question[3])

        await state.update_data(q4={
            'question_time': timer.get_time(),
            'question': text_question[3]
        })
        user_data = await state.get_data()
        await update_data_to_back(self.bot, user_data['message_id'], format_user_data(user_data))
        await state.set_state(OrderDailyServey.writting_question_4)

    async def question_handler_4(self, message: Message, state: FSMContext) -> None:
        await state.update_data(a4={
            'answer_time': timer.get_time(),
            'answer': message.text
        })

        await message.answer(text_question[4])

        await state.update_data(q5={
            'question_time': timer.get_time(),
            'question': text_question[4]
        })
        user_data = await state.get_data()
        await update_data_to_back(self.bot, user_data['message_id'], format_user_data(user_data))
        await state.set_state(OrderDailyServey.writting_question_5)

    async def question_handler_5(self, message: Message, state: FSMContext) -> None:
        await state.update_data(a5={
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

        # await wait_next_servey(self.bot, message.chat.id, state.storage)

import utils.timer as timer

from venv import logger

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from utils.data_register import data_register as dr
from back_chat.back_chat_utils import send_data_to_back
from utils.sheets.user_data_to_table import save_user_data

from .entry_servey_text import *
from .entry_servey_keyboards import *
from utils.service_text import text_error_try_again

router = Router()

class OrderIntroServey(StatesGroup):
    choosing_frequency = State()
    choosing_severity = State()

@router.callback_query(F.data == 'take_the_servey')
async def cmd_food(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(servey_type='entry')
    await state.update_data(date=timer.make_readable_date(timer.get_date()))
    await state.update_data(user_id=callback.from_user.id)

    await callback.answer(text_hint_begin)
    await callback.message.answer(text_begin) # type: ignore

    await callback.message.answer( # type: ignore
        text=text_question_1,
        reply_markup=get_first_question_keyboard()
    )
    await state.set_state(OrderIntroServey.choosing_frequency)


@router.callback_query(OrderIntroServey.choosing_frequency)
async def frequency_choosen(callback: CallbackQuery, state: FSMContext) -> None:
    if not callback.data or not callback.message:
        callback.answer(text_error_try_again)

        return
    
    await state.update_data(frequency=int(callback.data))
    await callback.answer(text_understand)
     
    await callback.message.answer( # type: ignore
        text=text_question_2,
        reply_markup=get_second_question_keyboard()
    )
    await state.set_state(OrderIntroServey.choosing_severity)


@router.callback_query(OrderIntroServey.choosing_severity)
async def severity_choosen(callback: CallbackQuery, state: FSMContext) -> None:
    if not callback.data or not callback.message:
        callback.answer(text_error_try_again)

        return
    
    name = ''
    if callback.from_user.first_name != None:
        name = callback.from_user.first_name
    if callback.from_user.last_name != None:
        name += ' ' + callback.from_user.last_name
    
    await state.update_data(severity=int(callback.data))
    await state.update_data(subscribe=True)
    await state.update_data(ud=str(callback.from_user))
    await state.update_data(name=name)
    await callback.answer(text_writen_down)

    user_data = await state.get_data()
    # logger.info('Server info: %s', user_data)
    dr.set_user_info(user_data['user_id'], user_data)

    await send_data_to_back(callback.bot, format_user_data(user_data))
    # save_user_data(user_data)

    await callback.message.answer( # type: ignore
        text=text_lets_begin_workig_together,
        reply_markup=get_entry_servey_continuation_keyboard()
    )

    await state.clear()

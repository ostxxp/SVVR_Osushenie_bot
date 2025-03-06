from aiogram import Router

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import inline_calendar
from bot.keyboards import back_to_objects

from months import months, months_selected

from states import States

import DB.database_funcs as db
import keyboards
from datetime import datetime

router = Router()


@router.callback_query()
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("obj_"):
        month = datetime.today().month
        year = datetime.today().year
        await callback.message.edit_text(f"Выберите дату для объекта\n*{callback.data.split('_', 2)[2]}*",
                                         parse_mode='Markdown',
                                         reply_markup=await inline_calendar.create_calendar(month, year, state))
    elif callback.data == "back_to_objects":
        keyboard = keyboards.objects_to_keyboard(callback.from_user.id)
        if keyboard is not None:
            await callback.message.edit_text("Здравствуй! Выбери объект:", reply_markup=keyboard)
    elif callback.data in "prev_monthnext_month" or callback.data.startswith("day_"):
        data = callback.data
        state_data = await state.get_data()
        month = state_data.get('month')
        year = state_data.get('year')

        if data == "prev_month":
            month -= 1
            if month < 1:
                month = 12
                year -= 1
            await callback.message.edit_text("Выберите день:",
                                             reply_markup=await inline_calendar.create_calendar(month, year, state))

        elif data == "next_month":
            month += 1
            if month > 12:
                month = 1
                year += 1
            await callback.message.edit_text("Выберите день:",
                                             reply_markup=await inline_calendar.create_calendar(month, year, state))

        elif data.startswith("day_"):
            day = int(data.split("_")[1])
            await callback.message.edit_text(f"Вы выбрали: *{day} {months_selected[month]} {year}*", parse_mode='Markdown',
                                             reply_markup=back_to_objects)

from calendar import month

from aiogram import Router, F
from aiogram.filters import or_f

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.testing import fails
from typer.cli import callback
from watchfiles import awatch

import inline_calendar
from bot.keyboards import back_to_objects
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from months import months, months_selected

from DB import groups_fetching

from states import States

import DB.database_funcs as db

from DB import prorabs_fetching
import keyboards
from datetime import datetime
from DB import database_funcs

router = Router()


@router.callback_query(F.data.startswith("obj_"))
async def select_object(callback: CallbackQuery, state: FSMContext):
    month = datetime.today().month
    year = datetime.today().year
    obj_name = callback.data.split('_', 2)[2]
    await callback.message.edit_text(f"Выберите дату для объекта\n*{obj_name}*",
                                     parse_mode='Markdown',
                                     reply_markup=await inline_calendar.create_calendar(month, year, state))


@router.callback_query(F.data == "back_to_objects")
async def back_to_objects(callback: CallbackQuery):
    keyboard = await keyboards.objects_to_keyboard(callback.from_user.id)
    if keyboard:
        await callback.message.edit_text("Выбери объект:", reply_markup=keyboard)


@router.callback_query(F.data == "prev_month")
async def prev_month(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    month, year = state_data.get('month', datetime.today().month), state_data.get('year', datetime.today().year)
    month -= 1
    if month < 1:
        month = 12
        year -= 1
    await callback.message.edit_text("Выберите день:",
                                     reply_markup=await inline_calendar.create_calendar(month, year, state))


@router.callback_query(F.data == "next_month")
async def next_month(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    month, year = state_data.get('month', datetime.today().month), state_data.get('year', datetime.today().year)
    month += 1
    if month > 12:
        month = 1
        year += 1
    await callback.message.edit_text("Выберите день:",
                                     reply_markup=await inline_calendar.create_calendar(month, year, state))


@router.callback_query(F.data.startswith("day_"))
async def select_day(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    month, year = state_data.get('month', datetime.today().month), state_data.get('year', datetime.today().year)
    day = int(callback.data.split("_")[1])
    await database_funcs.add_report(callback.from_user.id, f"{day}.{month}.{year}")
    keyboard = await keyboards.groups_to_keyboard(callback.from_user.id, True, 0)
    await callback.message.edit_text(
        f"Вы выбрали: *{day} {months_selected[month]} {year}*\n\nТеперь выберите группы работ, "
        f"которыми вы занимались, и, по готовности отчета, нажмите\n*Отправить📨*",
        parse_mode='Markdown', reply_markup=keyboard)


@router.callback_query(F.data.startswith("back_to_day_"))
async def groups_menu(callback: CallbackQuery, state: FSMContext):
    day, month, year = map(int, callback.data.split('_')[3].split('.'))
    keyboard = await keyboards.groups_to_keyboard(callback.from_user.id, True, 0)
    await callback.message.edit_text(
        f"Вы выбрали: *{day} {months_selected[month]} {year}*\n\nТеперь выберите группы работ, "
        f"которыми вы занимались, и, по готовности отчета, нажмите\n*Отправить📨*",
        parse_mode='Markdown', reply_markup=keyboard)


@router.callback_query(or_f(F.data.contains('.'), F.data.isdigit()))
async def subgroups(callback: CallbackQuery, state: FSMContext):
    keyboard = await keyboards.groups_to_keyboard(callback.from_user.id, False, callback.data.count('.') + 1,
                                                  callback.data)
    if len(keyboard.inline_keyboard) == 1:
        back = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data='.'.join(callback.data.split('.')[:-1]))]]
        )
        msg = await callback.message.edit_text(
            f"Вы выбрали:\n\n*{await groups_fetching.get_group_name(callback.data)}*.\n\n"
            f"Теперь укажите выполненный объем({await groups_fetching.get_work_type(callback.data)}). Напишите *только число*.",
            parse_mode='Markdown', reply_markup=back)
        await state.update_data(message=msg)
        await state.update_data(group=callback.data)
        await state.update_data(quantity=await groups_fetching.get_work_type(callback.data))
        await state.set_state(States.fill_volume)
    else:
        await callback.message.edit_text("Выберите подгруппу:", reply_markup=keyboard)

@router.message(States.fill_volume)
async def fill_volume(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = data.get('message')
    await message.delete()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data="confirm")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data=data.get('group'))],
        ]
    )
    await msg.edit_text(text=f"Объем: {message.text} ({data.get('quantity')}) Верно?", reply_markup=keyboard)

@router.callback_query(F.data == "confirm")
async def confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = data.get('message')
    await msg.edit_text(text="Выберите монтажников, которые присутствовали на объекте:", reply_markup=)
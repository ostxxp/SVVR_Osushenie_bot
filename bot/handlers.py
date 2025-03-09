from aiogram import Router, F

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import inline_calendar
from bot.keyboards import back_to_objects
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from months import months, months_selected

from states import States

import DB.database_funcs as db
import keyboards
from datetime import datetime
from DB import database_funcs

router = Router()


@router.callback_query(F.data == "prorab")
async def handle_prorab(callback: CallbackQuery, state: FSMContext):
    prorab = True
    if prorab:  # Есть ли прораб в таблице
        await database_funcs.add_prorab(callback.from_user.id)
        await callback.message.edit_text("Теперь вы зарегистрированы в боте. "
                                         "Чтобы заполнить дневной отчет по объекту напишите /fill "
                                         "(либо нажмите на эту команду)")


@router.callback_query(F.data == "installer")
async def handle_prorab(callback: CallbackQuery, state: FSMContext):
    installer = True
    if installer:  # Есть ли прораб в таблице
        await database_funcs.add_installer(callback.from_user.id)
        await callback.message.edit_text("Теперь вы зарегистрированы в боте. "
                                         "Вам будут приходить информационные сообщения о заполнении ведомостей прорабами")


@router.message(Command("fill"))
async def fill_report(message: Message, state: FSMContext):
    prorab = True
    if prorab:  # Прораб ли он
        # keyboard = keyboards.objects_to_keyboard(message.from_user.id)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Объект", callback_data="obj_id_Объект")]]
        )
        if keyboard is not None:
            await message.answer("Выбери объект:", reply_markup=keyboard)
        else:
            await message.answer("Похоже, что вы не прораб, либо вам не назначен ни один объект.")


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
    keyboard = keyboards.objects_to_keyboard(callback.from_user.id)
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
    await callback.message.edit_text(
        f"Вы выбрали: *{day} {months_selected[month]} {year}*\n\nТеперь выберите группы работ, "
        f"которыми вы занимались, и, по готовности отчета, нажмите\n*Отправить📨*",
        parse_mode='Markdown', reply_markup=keyboards.groups)

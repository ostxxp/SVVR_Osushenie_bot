from aiogram import Router, F
from aiogram.filters import or_f, and_f

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import inline_calendar
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from DB import report_table

from months import months_selected

from DB import groups_fetching, objects_fetching

from states import States

import keyboards
from datetime import datetime
from DB import database_funcs

router = Router()


@router.callback_query(F.data.startswith("obj_"))
async def select_object(callback: CallbackQuery, state: FSMContext):
    month = datetime.today().month
    year = datetime.today().year
    obj_name = callback.data.split('_', 2)[2]
    await database_funcs.add_report(id=callback.from_user.id, object_name=obj_name)
    await callback.message.edit_text(f"Выберите дату для объекта\n*{obj_name}*",
                                     parse_mode='Markdown',
                                     reply_markup=await inline_calendar.create_calendar(month, year, state))
    object = await objects_fetching.fetch_objects_by_name(obj_name)
    if object[3] == '':
        objects_fetching.add_link(f"D{int(object[0]) + 4}", await report_table.create_table_report(object[1]))


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
    keyboard = await keyboards.groups_to_keyboard(callback.from_user.id, True, 0)
    date = f"{day}.{month}.{year}"
    await database_funcs.add_date(callback.from_user.id, date)
    await callback.message.edit_text("Загрузка...")
    object = await objects_fetching.fetch_objects_by_name(await database_funcs.get_obj_name(callback.from_user.id))
    link = object[3]
    await report_table.fill_value(link, "G2", date)
    await callback.message.edit_text(
        f"Вы выбрали: *{day} {months_selected[month]} {year}*\n\nТеперь выберите группы работ, "
        f"которыми вы занимались, и, когда заполните все работы, нажмите\n*👨🏻‍🔧 Выбрать рабочих*",
        parse_mode='Markdown', reply_markup=keyboard)


@router.callback_query(F.data.startswith("back_to_day_"))
async def groups_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    day, month, year = map(int, callback.data.split('_')[3].split('.'))
    keyboard = await keyboards.groups_to_keyboard(callback.from_user.id, True, 0)
    await callback.message.edit_text(
        f"Вы выбрали: *{day} {months_selected[month]} {year}*\n\nТеперь выберите группы работ, "
        f"которыми вы занимались, и, когда заполните все работы, нажмите *👨🏻‍🔧 Выбрать рабочих*",
        parse_mode='Markdown', reply_markup=keyboard)


@router.callback_query(and_f(or_f(F.data.contains('.'), F.data.isdigit())), F.data[0].isdigit())
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
            [InlineKeyboardButton(text="✅ Да",
                                  callback_data=f"back_to_day_{await database_funcs.get_report_date(message.from_user.id)}")]
        ]
    )
    try:
        a = int(message.text)
        try:
            await msg.edit_text("Загрузка...")
            object = await objects_fetching.fetch_objects_by_name(await database_funcs.get_obj_name(message.from_user.id))
            link = object[3]
            location = await report_table.find_row(link, data.get('group'))
            value = message.text
            await report_table.fill_value(link, location, value)
            await msg.edit_text(
                text=f"Объем: {message.text} ({data.get('quantity')}) Верно?\nЕсли нет, напишите значение ещё раз",
                reply_markup=keyboard)
        except:
            pass
    except:
        try:
            await msg.edit_text(text=f"Нужно указать только число.")
        except:
            pass


@router.callback_query(F.data == "installers")
async def confirm(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Выберите монтажников, которые присутствовали на объекте:",
                                     reply_markup=await keyboards.installers_to_keyboard(callback.from_user.id))


@router.callback_query(F.data.startswith("installer_"))
async def installer_selection(callback: CallbackQuery, state: FSMContext):
    installer = callback.data.split('_')[1]
    installers = await database_funcs.get_installers(callback.from_user.id)
    if installers and installer in installers:
        await database_funcs.remove_installer(callback.from_user.id, installer)
    else:
        await database_funcs.add_installer(callback.from_user.id, installer)
    await callback.message.edit_text(text="Выберите монтажников, которые присутствовали на объекте:",
                                     reply_markup=await keyboards.installers_to_keyboard(callback.from_user.id))


@router.callback_query(F.data.startswith("submit_"))
async def submit(callback: CallbackQuery, state: FSMContext):
    day, month, year = map(int, callback.data.split('_')[1].split('.'))
    await callback.message.edit_text(f"✅ Дневной отчет за *{day} {months_selected[month]} {year}* заполнен!"
                                     f"\nЧтобы заполнить ещё один отчет, напишите команду /start",
                                     parse_mode='Markdown')
    await database_funcs.filled(callback.from_user.id, True)
    await database_funcs.clear_reports(callback.from_user.id)

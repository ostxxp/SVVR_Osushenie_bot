from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.filters import or_f, and_f
import os

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot import inline_calendar, keyboards
from bot.months import months_selected
from bot.states import States

from bot.bot_init import bot

from DB import groups_fetching, objects_fetching, prorabs_fetching, fill_feedback, database_funcs, report_table

router = Router()


@router.callback_query(F.data.startswith("obj_"))
async def select_object(callback: CallbackQuery, state: FSMContext):
    month = datetime.today().month
    year = datetime.today().year
    obj_name = callback.data.split('_', 2)[2]

    await database_funcs.add_report(id=callback.from_user.id, object_name=obj_name,
                                    prorab_name=await prorabs_fetching.get_prorab_name(callback.from_user.id))
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
    await callback.message.edit_text(f"Секунду...",
                                     parse_mode='Markdown')
    state_data = await state.get_data()

    month, year = state_data.get('month', datetime.today().month), state_data.get('year', datetime.today().year)
    day = callback.data.split("_")[1]

    str_month = str(month)
    if len(day) == 1:
        day = '0' + day
    if len(str_month) == 1:
        str_month = '0' + str_month

    date = f"{day}.{str_month}.{year}"

    with open(f'report_info/{callback.from_user.id}.txt', 'w', encoding='utf-8') as file:
        file.write(date + '\n')

    await database_funcs.add_date(callback.from_user.id, date)

    obj = await objects_fetching.fetch_objects_by_name(await database_funcs.get_obj_name(callback.from_user.id))
    link = obj[3]
    if await report_table.find_date(callback.from_user.id, link, date) == "exists":
        await callback.message.edit_text(
            f"👨🏻‍🔧 Дневной отчет за *{day} {months_selected[month]} {year}* уже был заполнен!"
            f"\nЧтобы заполнить ещё один отчет, напишите команду /start",
            parse_mode='Markdown')
        try:
            await database_funcs.clear_reports(callback.from_user.id)
            os.remove(f"report_info/{callback.from_user.id}.txt")
        except FileNotFoundError:
            print(f"The file report_info/{callback.from_user.id}.txt was not found")
    else:
        await callback.message.edit_text(f"Проводились ли работы *{day} {months_selected[month]} {year}*?",
                                         reply_markup=keyboards.yes_no_keyboard, parse_mode='Markdown')


@router.callback_query(F.data == "yes")
async def yes(callback: CallbackQuery):
    keyboard = await keyboards.groups_to_keyboard(callback.from_user.id, True, 0)

    day, month, year = map(int, (await database_funcs.get_report_date(callback.from_user.id)).split('.'))
    str_day = str(day)
    if len(str(day)) == 1:
        str_day = '0' + str_day
    await callback.message.edit_text(
        f"Вы выбрали: *{str_day} {months_selected[month]} {year}*\n\nТеперь выберите группы работ, "
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

    if len(keyboard.inline_keyboard) == 2:
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
        a = float(message.text.replace(',', '.'))
        try:
            await msg.edit_text(
                text=f"Объем: {message.text} ({data.get('quantity')}) Верно?\nЕсли нет, напишите значение ещё раз",
                reply_markup=keyboard)
            with open(f"report_info/{message.from_user.id}.txt", 'a', encoding='utf-8') as file:
                file.write(f'{data.get('group')} {message.text.replace(',', '.')}\n')
        except Exception as e:
            print(e)
    except:
        try:
            await msg.edit_text(text=f"Нужно указать только число. Попробуйте ещё раз")
        except Exception as e:
            print(e)


@router.callback_query(F.data == "installers")
async def confirm(callback: CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text(text="Выберите монтажников, которые присутствовали на объекте:\n\n"
                                                "_(Вы можете отфильтровать рабочих по фамилии. Для этого просто "
                                                "напишите желаемое начало фамилии работника)_",
                                           reply_markup=await keyboards.installers_to_keyboard(callback.from_user.id),
                                           parse_mode='Markdown')
    await state.update_data(message=msg)
    await state.set_state(States.wait_for_filter)


@router.message(States.wait_for_filter)
async def wait_for_filter(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    msg = data.get('message')

    await msg.edit_text(text=f"Работники, имена которых начинаются с {message.text}:",
                        reply_markup=await keyboards.installers_to_keyboard(message.from_user.id,
                                                                            message.text.lower().strip()))


@router.callback_query(F.data.startswith("installer_"))
async def installer_selection(callback: CallbackQuery):
    installer = callback.data.split('_')[1]
    installers = await database_funcs.get_installers(callback.from_user.id)

    if installers and installer in installers:
        await database_funcs.remove_installer(callback.from_user.id, installer)
    else:
        await database_funcs.add_installer(callback.from_user.id, installer)
    msg = await callback.message.edit_text(text="Выберите монтажников, которые присутствовали на объекте:\n\n"
                                                "_(Вы можете отфильтровать рабочих по фамилии. Для этого просто "
                                                "напишите желаемое начало фамилии работника)_",
                                           reply_markup=await keyboards.installers_to_keyboard(callback.from_user.id),
                                           parse_mode='Markdown')


@router.callback_query(F.data.startswith("submit_"))
async def submit(callback: CallbackQuery):
    await callback.message.edit_text("Загружаю данные в таблицу...")
    day, month, year = map(int, (await database_funcs.get_report_date(callback.from_user.id)).split('.'))
    if callback.data.split('_')[1] != 'no':
        with open(f'report_info/{callback.from_user.id}.txt', 'a', encoding='utf-8') as file:
            file.write(f"{(await database_funcs.get_installers(callback.from_user.id))[:-1]}")

    with open(f'report_info/{callback.from_user.id}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if len(lines) > 1:
        work_done = ""
        for k in range(1, len(lines) - 1):
            work_done += f"*{lines[k].split()[0].strip()}. {await groups_fetching.get_group_name(lines[k].split()[0].strip())}:* {lines[k].split()[1].strip()} {await groups_fetching.get_work_type(lines[k].split()[0].strip())}\n\n"
        work_done += "\n*Монтажники:*\n" + "\n".join(sorted(lines[-1].split(',')))
    else:
        work_done = "❌ Работы не проводились"

    await report_table.create_table_report(callback.from_user.id)
    object = await database_funcs.get_obj_name(callback.from_user.id)
    str_day = str(day)
    if len(str(day)) == 1:
        str_day = '0' + str_day

    await bot.send_message(chat_id="@osusheniebot",
                           text=f"Отчет по объекту *{object}* от {await prorabs_fetching.get_prorab_name(callback.from_user.id)} за *{lines[0].strip()}*:\n\n{work_done}", parse_mode="Markdown")

    await callback.message.edit_text(
        f"✅Дневной отчет по объекту\n*{object}* за *{str_day} {months_selected[month]} {year}* заполнен!\n"
        f"\nЧтобы заполнить ещё один отчет, напишите команду /start",
        parse_mode='Markdown')

    if day == datetime.today().day and month == datetime.today().month and year == datetime.today().year:
        object_name = await database_funcs.get_obj_name(callback.from_user.id)
        await database_funcs.object_filled(callback.from_user.id, object_name)

    await database_funcs.clear_reports(callback.from_user.id)

    try:
        os.remove(f"report_info/{callback.from_user.id}.txt")
    except FileNotFoundError:
        print(f"The file report_info/{callback.from_user.id}.txt was not found")


@router.callback_query(F.data == "abort")
async def abort(callback: CallbackQuery):
    await database_funcs.clear_reports(callback.from_user.id)
    try:
        os.remove(f"report_info/{callback.from_user.id}.txt")
    except FileNotFoundError:
        print(f"The file report_info/{callback.from_user.id}.txt was not found")
    await callback.message.edit_text("❌ Заполнение прервано, чтобы заполнить новый отчет, нажмите /start")


@router.callback_query(or_f(F.data == "feedback", F.data == "feedback_no"))
async def ask_for_feedback(callback: CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text("Просто напишите Ваше сообщение и я передам его руководителю.")
    await state.update_data(feedback_message=msg)
    await state.set_state(States.wait_for_feedback)


@router.callback_query(F.data == "feedback_yes")
async def apply_feedback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Передаю данные...")

    try:
        await fill_feedback.add_feedback(callback.from_user.id)
        os.remove(f"feedbacks_temp/{callback.from_user.id}.txt")
        await callback.message.edit_text(
            "✅ Готово!\nЯ всё передал  🫡\n\nВаше сообщение будет рассмотрено в ближайшее время.\n\nПерейти в главное меню 👉  /start",
            reply_markup=keyboards.feedback_keyboard)
    except Exception as e:
        await bot.send_message(403953652,
                               f"❗️ОШИБКА ПРИ ИСПОЛНЕНИИ ОТ @{callback.from_user.username} (id = {callback.from_user.id})\n\n{e}")
        await callback.message.edit_text("❗️ В ходе заполнения вышла ошибка", reply_markup=keyboards.feedback_keyboard)


@router.message(States.wait_for_feedback)
async def feedback(message: Message, state: FSMContext):
    await message.delete()
    state_data = await state.get_data()
    msg = state_data.get('feedback_message')
    await msg.edit_text(
        f"Ваши предложения / идеи / пожелания:\n\n*{message.text}*\n\nЕсли хотите изменить текст, просто напишите сообщение еще раз, нажимать на кнопку не нужно)",
        parse_mode='markdown', reply_markup=keyboards.yes_no_feedback_keyboard)
    with open(f"feedbacks_temp/{message.from_user.id}.txt", 'w', encoding='utf-8') as file:
        t = datetime.today() + timedelta(hours=3)

        if len(str(t.day)) == 1:
            day = f"0{t.day}"
        else:
            day = str(t.day)

        if len(str(t.month)) == 1:
            month = f"0{t.month}"
        else:
            month = str(t.month)

        if len(str(t.hour)) == 1:
            hour = f"0{t.hour}"
        else:
            hour = str(t.hour)

        if len(str(t.minute)) == 1:
            minute = f"0{t.minute}"
        else:
            minute = str(t.minute)

        if message.from_user.username is None:
            if message.from_user.first_name is not None:
                username = f"{message.from_user.first_name}"
                if message.from_user.last_name is not None:
                    username += f" {message.from_user.last_name}"
            else:
                username = f"Нет данных"
        else:
            username = f"@{message.from_user.username}"

        file.write(f'{day}.{month}.{t.year}|{hour}:{minute}|{username}|{message.text}')

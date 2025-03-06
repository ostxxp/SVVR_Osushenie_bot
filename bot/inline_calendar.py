import calendar
from aiogram import Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from months import months

router = Router()

async def create_calendar(month, year, state: FSMContext):
    await state.update_data(month=month)
    await state.update_data(year=year)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    month_days = calendar.monthcalendar(year, month)

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="←", callback_data="prev_month"),
        InlineKeyboardButton(text=f"{months[month]} {year}", callback_data="none"),
        InlineKeyboardButton(text="→", callback_data="next_month")
    ])

    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="empty"))
            else:
                row.append(InlineKeyboardButton(text=str(day), callback_data=f"day_{day}"))
        keyboard.inline_keyboard.append(row)

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="<-- Вернуться к объектам", callback_data="back_to_objects")
    ])

    return keyboard
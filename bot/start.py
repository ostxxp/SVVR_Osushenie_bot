from aiogram import Router
import asyncio
from bot.reminder import send_reminders

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import database_funcs, objects_fetching

from bot import keyboards

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await database_funcs.clear_reports(message.from_user.id)
    keyboard = await keyboards.objects_to_keyboard(message.from_user.id)
    if keyboard is not None and len(keyboard.inline_keyboard) > 1:
        await message.answer("Здравствуй! Выбери объект:", reply_markup=keyboard)
        if not await database_funcs.prorab_exists(message.from_user.id):
            await database_funcs.add_prorab(message.from_user.id)
            object_names = await objects_fetching.fetch_objects_names(message.from_user.id)
            object_names.append("")
            object_names = "|".join(object_names)
            await database_funcs.set_objects(message.from_user.id, object_names)

            loop = asyncio.get_event_loop()
            loop.create_task(send_reminders(message.from_user.id))
    else:
        await message.answer("Похоже, что Вы не прораб, либо Вам не назначен ни один объект.\n\nНо! Вы можете отправить своё пожелание, предложение по улучшению нашей компании\n\nТут 👇🏻", reply_markup=keyboards.feedback_keyboard)

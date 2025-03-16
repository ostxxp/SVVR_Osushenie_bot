from aiogram import Router
import asyncio
from bot.reminder import send_reminders

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import database_funcs

from bot import keyboards

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await database_funcs.clear_reports(message.from_user.id)
    keyboard = await keyboards.objects_to_keyboard(message.from_user.id)
    if keyboard is not None:
        await message.answer("Здравствуй! Выбери объект:", reply_markup=keyboard)
        if not await database_funcs.prorab_exists(message.from_user.id):
            loop = asyncio.get_event_loop()
            loop.create_task(send_reminders(message.from_user.id))
            await database_funcs.add_prorab(message.from_user.id)
    else:
        await message.answer("Похоже, что вы не прораб, либо вам не назначен ни один объект.")


from aiogram import Router

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import database_funcs

import keyboards

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    keyboard = await keyboards.objects_to_keyboard(message.from_user.id)
    if keyboard is not None:
        await message.answer("Здравствуй! Выбери объект:", reply_markup=keyboard)
    else:
        await message.answer("Похоже, что вы не прораб, либо вам не назначен ни один объект.")


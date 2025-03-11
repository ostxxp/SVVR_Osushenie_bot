from aiogram import Router

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import database_funcs

import keyboards
from DB.prorabs_fetching import prorabs

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    keyboard = await keyboards.objects_to_keyboard(message.from_user.id)
    if keyboard is not None:
        await message.answer("Здравствуй! Выбери объект:", reply_markup=keyboard)
        if not await database_funcs.prorab_exists(message.from_user.id):
            await database_funcs.add_prorab(message.from_user.id)
    else:
        await message.answer("Похоже, что вы не прораб, либо вам не назначен ни один объект.")


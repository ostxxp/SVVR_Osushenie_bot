from aiogram import Router

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import database_funcs

import keyboards

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if await database_funcs.prorab_exists(message.from_user.id):
        await message.answer(
            "Вы уже зарегистрировались в боте. Чтобы заполнить дневной отчет по объекту напишите /fill "
            "(либо нажмите на эту команду)")
    elif await database_funcs.installer_exists(message.from_user.id):
        await message.answer("Вы уже зарегистрировались в боте.")
    else:
        await message.answer("Для регистрации в боте выберите свою роль:", reply_markup=keyboards.role)

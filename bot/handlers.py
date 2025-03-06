from aiogram import Router

from aiogram.filters import Command
from aiogram.types import Message
import DB.database as db

router = Router()

@router.message(Command("edit"))
async def edit(message: Message):
    if await db.is_admin(message.from_user.id):
        await message.answer("Что нужно поменять?")
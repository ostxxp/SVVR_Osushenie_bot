from aiogram import Router

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.methods.edit_message_text import EditMessageText

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from __init__ import bot

import keyboards

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    keyboard = keyboards.objects_to_keyboard(message.from_user.id)
    if keyboard is not None:
        await message.answer("Здравствуй! Выбери объект:", reply_markup=keyboard)
    else:
        await message.answer("Похоже, что вы не прораб, либо вам не назначен ни один объект")

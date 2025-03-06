from aiogram import Router

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.fsm.context import FSMContext

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from __init__ import bot

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Здравствуй!")
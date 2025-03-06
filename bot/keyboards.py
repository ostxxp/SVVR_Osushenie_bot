from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

edit_list = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Добавить прораба", callback_data="add_prorab"),
                      InlineKeyboardButton(text="Удалить прораба", callback_data="remove_prorab")],
                     [InlineKeyboardButton(text="Настройки администраторов", callback_data="admin_settings")]]
)

back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")]],
)



button1 = InlineKeyboardButton(text="Кнопка 1", callback_data="button1")
keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1]])
keyboard.add(button1)

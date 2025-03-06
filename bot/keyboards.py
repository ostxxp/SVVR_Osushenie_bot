from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import DB.objects_fetching as of

edit_list = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Добавить прораба", callback_data="add_prorab"),
                      InlineKeyboardButton(text="Удалить прораба", callback_data="remove_prorab")],
                     [InlineKeyboardButton(text="Настройки администраторов", callback_data="admin_settings")]]
)

back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")]],
)

def objects_to_keyboard(id):
    buttons = []
    for obj in of.fetch_objects(id):
        buttons.append([InlineKeyboardButton(text=obj, callback_data=f"obj_{id}_{obj}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

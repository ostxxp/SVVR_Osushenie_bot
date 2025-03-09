from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# import DB.objects_fetching as of

edit_list = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Добавить прораба", callback_data="add_prorab"),
                      InlineKeyboardButton(text="Удалить прораба", callback_data="remove_prorab")],
                     [InlineKeyboardButton(text="Настройки администраторов", callback_data="admin_settings")]]
)

back_to_objects = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="<-- Вернуться к объектам", callback_data="back_to_objects")]],
)

role = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Я - прораб", callback_data="prorab"),
                      InlineKeyboardButton(text="Я - монтажник", callback_data="installer")]],
)

# def objects_to_keyboard(id):
#     buttons = []
#     if of.fetch_objects(id) is not None:
#         for obj in of.fetch_objects(id):
#             buttons.append([InlineKeyboardButton(text=obj, callback_data=f"obj_{id}_{obj}")])
#         keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#         return keyboard
#     return None

groups = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Иглофильтры", callback_data="Иглофильтры")],
                     [InlineKeyboardButton(text="Отправить📨", callback_data="send_report")]]
)
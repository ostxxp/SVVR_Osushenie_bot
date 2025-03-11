from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import DB.objects_fetching as of
import DB.groups_fetching as grps

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

try_prorab_again = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="🔁 Повторить попытку", callback_data="prorab")]]
)

async def objects_to_keyboard(id):
    buttons = []
    if of.fetch_objects(id) is not None:
        for obj in of.fetch_objects(id):
            buttons.append([InlineKeyboardButton(text=obj, callback_data=f"obj_{id}_{obj}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
    return None

async def groups_to_keyboard(is_general, iteration, group_number = None):
    buttons = []
    groups = grps.groups
    print(group_number)
    for group in groups:
        if group[0].count('.') == iteration:
            if group_number is None or group[0].startswith(f"{group_number}."):
                buttons.append([InlineKeyboardButton(text=f"{group[0].split('.')[iteration]}. {group[1]}", callback_data=group[0])])

    if is_general:
        buttons.append([InlineKeyboardButton(text="Отправить📨", callback_data="send_report")])
    else:
        try:
            buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"{group_number[:-2]}")])
        except:
            buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"{group_number[:-2]}")])
    groups = InlineKeyboardMarkup(inline_keyboard=buttons)
    return groups

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from DB import objects_fetching, groups_fetching, database_funcs
from DB import installers_fetching

yes_no_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="✅ Да", callback_data="yes"),
                      InlineKeyboardButton(text="❌ Нет", callback_data="submit_no")]]
)

async def objects_to_keyboard(id):
    buttons = []
    if (await objects_fetching.fetch_objects_names(id)) is not None:
        for obj in (await objects_fetching.fetch_objects_names(id)):
            buttons.append([InlineKeyboardButton(text=obj, callback_data=f"obj_{id}_{obj}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
    return None

async def groups_to_keyboard(id, is_general, iteration, group_number = None):
    buttons = []
    groups = groups_fetching.sorted_groups
    for group in groups:
        if group[0].count('.') == iteration:
            if group_number is None or group[0].startswith(f"{group_number}."):
                if len(group[1]) > 85:
                    name = f"{group[1][:85]}..."
                else:
                    name = group[1]
                buttons.append([InlineKeyboardButton(text=f"{group[0]}. {name}", callback_data=group[0])])

    if is_general:
        buttons.append([InlineKeyboardButton(text="👨🏻‍🔧 Выбрать рабочих", callback_data="installers")])
    elif group_number.count('.') > 0:
        num = '.'.join(group_number.split('.')[:-1])
        buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=num)])
    else:
        buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_day_{await database_funcs.get_report_date(id)}")])
    groups = InlineKeyboardMarkup(inline_keyboard=buttons)
    return groups

async def installers_to_keyboard(id, filter=None):
    buttons = []
    if filter is None:
        k = 0
        for installer in installers_fetching.installers:
            if k < 3:
                inst = str(installer[1])
                if (await database_funcs.get_installers(id) is not None) and installer[1] in (await database_funcs.get_installers(id)):
                    inst = "✅ " + inst
                buttons.append([InlineKeyboardButton(text=inst, callback_data=f"installer_{installer[1]}")])
                k += 1
            else:
                inst = str(installer[1])
                if (await database_funcs.get_installers(id) is not None) and installer[1] in (await database_funcs.get_installers(id)):
                    inst = "✅ " + inst
                    buttons.append([InlineKeyboardButton(text=inst, callback_data=f"installer_{installer[1]}")])

        buttons.append(
            [InlineKeyboardButton(text="...", callback_data=f"none")]
        )
    else:
        for installer in installers_fetching.installers:
            inst = str(installer[1])
            if inst.lower().startswith(filter):
                if (await database_funcs.get_installers(id) is not None) and installer[1] in (await database_funcs.get_installers(id)):
                    inst = "✅ " + inst
                buttons.append([InlineKeyboardButton(text=inst, callback_data=f"installer_{installer[1]}")])
    buttons.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_day_{await database_funcs.get_report_date(id)}")])
    buttons.append([InlineKeyboardButton(text="Отправить📨", callback_data=f"submit_{await database_funcs.get_report_date(id)}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

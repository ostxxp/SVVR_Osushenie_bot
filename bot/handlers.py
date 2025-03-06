from aiogram import Router

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from states import States

import DB.database_funcs as db
import keyboards

router = Router()


@router.message(Command("edit"))
async def edit(message: Message, state: FSMContext):
    if db.is_admin(message.from_user.id):
        await message.answer("Что нужно поменять?", reply_markup=keyboards.edit_list)


@router.callback_query()
async def query_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(callback_data=callback)
    if callback.data == "back_to_menu":
        await callback.message.edit_text("Что нужно поменять?", reply_markup=keyboards.edit_list)
        await state.set_state(States.edit)
    elif callback.data == "add_prorab":
        await callback.answer("")
        await callback.message.edit_text("Введите телеграм id нового прораба", reply_markup=keyboards.back_to_menu)
        await state.set_state(States.prorab_add_id)
    elif callback.data == "remove_prorab":
        await callback.answer("")
        await callback.message.edit_text("Введите телеграм id прораба, которого хотите удалить",
                                         reply_markup=keyboards.back_to_menu)
        await state.set_state(States.prorab_remove_id)


@router.message(States.prorab_add_id)
async def add_prorab_1(message: Message, state: FSMContext):
    data = await state.get_data()
    callback = data.get("callback_data")
    try:
        await message.delete()
        id = int(message.text)
        await state.update_data(prorab_add_id=id)
        await callback.message.edit_text(f"Id: *{id}*\nТеперь введите имя нового прораба в формате: _Крышковец Н._",
                                         parse_mode='Markdown',
                                         reply_markup=keyboards.back_to_menu)
        await state.set_state(States.prorab_add_id)
    except:
        await callback.message.edit_text(f"Id должен содержать только цифры. Попробуйте еще раз",
                                         reply_markup=keyboards.back_to_menu)


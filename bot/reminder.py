import asyncio
from datetime import datetime, timedelta

from bot.bot_init import bot
from DB import database_funcs, objects_fetching, prorabs_fetching

from bot import keyboards


async def send_reminders(id):
    while True:
        keyboard = await keyboards.objects_to_keyboard(id)
        if keyboard is None or len(keyboard.inline_keyboard) == 0:
            now = datetime.now()
            target_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
            if now > target_time:
                target_time += timedelta(days=1)

            secs = (target_time - now).total_seconds()
            await asyncio.sleep(secs)
            continue
        still_working = False
        for prorab in await prorabs_fetching.get_prorabs():
            if prorab[0] == str(id):
                still_working = True
                break
        if not still_working:
            await database_funcs.remove_prorab(id)
            break
        if not await database_funcs.prorab_exists(id):
            break
        now = datetime.now()
        hour = (now.hour + 3) % 24
        if hour >= 20:
            if now.minute % 15 == 0:
                if not await database_funcs.is_filled(id):
                    unfilled_objects = await database_funcs.get_unfilled_objects(id)
                    await bot.send_message(chat_id=id,
                                           text="‼️ Пожалуйста, заполните дневной отчет по объектам ‼️",
                                           reply_markup=await keyboards.objects_to_keyboard_by_names(id, unfilled_objects))
                    await asyncio.sleep(900)
                else:
                    target_time = now.replace(hour=21, minute=0, second=0, microsecond=0)
                    secs = (target_time - now).total_seconds()
                    await asyncio.sleep(secs)
            else:
                if now.minute > 45:
                    if hour == 23:
                        target_time = now.replace(hour=21, minute=0, second=0, microsecond=0)
                    else:
                        target_time = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)
                else:
                    target_time = now.replace(hour=now.hour, minute=15 * (now.minute // 15 + 1), second=0,
                                              microsecond=0)
                secs = (target_time - now).total_seconds()
                await asyncio.sleep(secs)
        else:
            objs = await objects_fetching.fetch_objects_names(id)
            objs.append("")
            await database_funcs.set_objects(id, "|".join(objs))
            await database_funcs.filled(id, False)
            now = datetime.now()
            target_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
            if now > target_time:
                target_time += timedelta(days=1)

            secs = (target_time - now).total_seconds()
            await asyncio.sleep(secs)

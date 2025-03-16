import asyncio
from datetime import datetime, timedelta

from bot.bot_init import bot
from DB import database_funcs


async def send_reminders(id):
    while True:
        now = datetime.now()
        if now.hour >= 20:
            if now.minute % 15 == 0:
                if not await database_funcs.is_filled(id):
                    await bot.send_message(chat_id=id, text="‼️ Пожалуйста, заполните дневной отчет по объекту ‼️")
                    await asyncio.sleep(900)
                else:
                    target_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    secs = (target_time - now).total_seconds()
                    await asyncio.sleep(secs)
                    await database_funcs.filled(id, False)
            else:
                if now.minute > 45:
                    if now.hour == 23:
                        target_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    else:
                        target_time = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)
                else:
                    target_time = now.replace(hour=now.hour, minute=15 * (now.minute // 15 + 1), second=0,
                                              microsecond=0)
                secs = (target_time - now).total_seconds()
                await asyncio.sleep(secs)
        else:
            now = datetime.now()
            target_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
            if now > target_time:
                target_time += timedelta(days=1)

            secs = (target_time - now).total_seconds()
            await asyncio.sleep(secs)

import asyncio
from datetime import datetime, timedelta

from __init__ import bot
from DB import database_funcs

async def send_reminders(id):
    while True:
        now = datetime.now()
        if now.hour >= 20:
            if not await database_funcs.is_filled(id):
                await bot.send_message(chat_id=id, text="‼️ Пожалуйста, заполните дневной отчет по объекту ‼️")
                await asyncio.sleep(900)
        else:
            now = datetime.now()
            target_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
            if now > target_time:
                target_time += timedelta(days=1)

            secs = (target_time - now).total_seconds()
            print(secs)
            await asyncio.sleep(secs)


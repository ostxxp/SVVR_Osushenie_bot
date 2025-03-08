import asyncio
from datetime import datetime, timedelta
from __init__ import bot

async def send_reminders(id):
    while True:
        now = datetime.now()
        if now.hour == 18 and now.minute >= 40:
            await bot.send_message(chat_id=id, text="хай")
            await asyncio.sleep(300)
        else:
            now = datetime.now()
            target_time = now.replace(hour=18, minute=40, second=0, microsecond=0)
            if now > target_time:
                target_time += timedelta(days=1)

            secs = (target_time - now).total_seconds()
            print(secs)
            await asyncio.sleep(secs)


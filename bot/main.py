import asyncio


import start, handlers
import inline_calendar
from __init__ import dp, bot
import reminder
from DB import database_funcs


async def main():
    dp.include_routers(
        start.router,
        handlers.router,
        inline_calendar.router
    )
    loop = asyncio.get_event_loop()
    prorabs = await database_funcs.get_prorabs()
    for prorab in prorabs:
        loop.create_task(reminder.send_reminders(prorab.id))
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")

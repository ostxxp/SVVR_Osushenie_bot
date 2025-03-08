import asyncio

import start, handlers
import inline_calendar
from __init__ import dp, bot
import reminder


async def main():
    dp.include_routers(
        start.router,
        handlers.router,
        inline_calendar.router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Бот запущен")
        loop = asyncio.get_event_loop()
        loop.create_task(reminder.send_reminders(123))
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")

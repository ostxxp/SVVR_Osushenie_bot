import asyncio

import start, handlers
import inline_calendar
from __init__ import dp, bot


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
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")

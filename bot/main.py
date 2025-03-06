import asyncio

import start, handlers
from __init__ import dp, bot


async def main():
    dp.include_routers(
        start.router,
        handlers.router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Бот запущен")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")

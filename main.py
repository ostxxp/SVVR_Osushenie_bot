import asyncio


from bot import start, handlers
from bot import inline_calendar
from bot.bot_init import dp, bot
from bot.reminder import send_reminders
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
        loop.create_task(send_reminders(prorab.id))
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")

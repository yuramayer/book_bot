import asyncio
from handlers import start, dummy
from bot import bot, dp


async def main():
    dp.include_routers(start.start_router, dummy.dummy_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


import asyncio
from handlers import start, dummy, translator
from bot import bot, dp
from utils.starting import on_startup

async def main():
    dp.include_routers(start.start_router, dummy.dummy_router, translator.translation_router)
    dp.startup.register(on_startup)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


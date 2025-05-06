"""Starting Telegram bot app"""

import asyncio
from handlers import start_router, cancel_router, new_page_router, \
    choice_router, read_page_router, left_router, right_router, \
    translation_router, dummy_router
from bot import bot, dp
from utils.starting import on_startup


async def main():
    """Bot startup function"""
    dp.include_routers(start_router, cancel_router, new_page_router,
                       choice_router, read_page_router, left_router,
                       right_router, translation_router, dummy_router)
    dp.startup.register(on_startup)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

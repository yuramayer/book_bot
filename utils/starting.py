"""Methods running when the bot is starting"""

import logging
from bot import bot
from back.db_back import is_checked_db, create_books_database, \
    create_books_table, create_current_books_table, create_book_len_table
from config.conf import admins_ids


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - \
                        %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def on_startup():
    """When bot is started, check db & send message to the admins"""

    for admin_id in admins_ids:
        try:
            await bot.send_message(admin_id, 'Бот включён 😎')
        except Exception as err:
            logger.info(
                "There was a problem with an id %s: %s",
                admin_id,
                err
            )

    create_books_database()
    create_books_table()
    create_current_books_table()
    create_book_len_table()

    if not await is_checked_db():
        for admin_id in admins_ids:
            try:
                await bot.send_message(admin_id,
                                       'База данных не работает 😢')
            except Exception as err:
                logger.info(
                    "There was a problem with an id %s: %s",
                    admin_id,
                    err
                )
        return

    for admin_id in admins_ids:
        try:
            await bot.send_message(admin_id,
                                   'База данных успешно подключена 🤗')
        except Exception as err:
            logger.info(
                "There was a problem with an id %s: %s",
                admin_id,
                err
            )

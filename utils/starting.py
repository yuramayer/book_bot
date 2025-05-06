"""Methods running when the bot is starting"""

from bot import bot
from back.db_back import is_checked_db, create_books_database, \
    create_books_table, create_current_books_table, create_book_len_table
from config.conf import admins_ids


async def on_startup():
    """When bot is started, check db & send message to the admins"""

    for admin_id in admins_ids:
        await bot.send_message(admin_id, 'Бот включён 😎')

    create_books_database()
    create_books_table()
    create_current_books_table()
    create_book_len_table()

    if not is_checked_db:
        for admin_id in admins_ids:
            await bot.send_message(admin_id, 'База данных не работает 😢')
        return

    for admin_id in admins_ids:
        await bot.send_message(admin_id, 'База данных успешно подключена 🤗')

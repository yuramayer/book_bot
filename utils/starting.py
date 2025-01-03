from bot import bot
from back.db_back import is_checked_db
from config.conf import admins_ids


async def on_startup():

    for admin_id in admins_ids:
            await bot.send_message(admin_id, 'Бот включён 😎')        

    if not is_checked_db:
        for admin_id in admins_ids:
            await bot.send_message(admin_id, 'База данных не подключена 😢')
        return 
    
    for admin_id in admins_ids:
            await bot.send_message(admin_id, 'База данных успешно подключена 🤗')
        
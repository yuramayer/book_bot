from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

def get_checked_env(env_name):
    env = os.getenv(env_name)
    if not env:
        raise RuntimeError(f"The required variable isn't defined: {env_name}")
    return str(env)     

BOT_TOKEN = get_checked_env('BOT_TOKEN')
BOOKS = get_checked_env('BOOKS')
BOOKS_PATHS = get_checked_env('BOOKS_PATH')
ADMINS = get_checked_env('ADMINS')
DB_PATH = get_checked_env('DB_PATH')
OPENAI_TOKEN = get_checked_env('OPENAI_TOKEN')


admins_ids = [int(admin_id) for admin_id in ADMINS.split(',')]
bks = [str(book) for book in BOOKS.split(';')]
pths = [str(book_path) for book_path in BOOKS_PATHS.split(';')]
books = dict(zip(bks, pths))

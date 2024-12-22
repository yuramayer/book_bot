from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
BOOKS = str(os.getenv('BOOKS'))
BOOKS_PATHS = str(os.getenv('BOOKS_PATH'))
ADMINS = str(os.getenv('ADMINS'))
DB_LINK = str(os.getenv('DB_LINK'))

admins_ids = [int(admin_id) for admin_id in ADMINS.split(',')]
bks = [str(book) for book in BOOKS.split(';')]
pths = [str(book_path) for book_path in BOOKS_PATHS.split(';')]
books = dict(zip(bks, pths)) 


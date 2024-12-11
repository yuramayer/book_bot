from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
BOOKS = str(os.getenv('BOOKS'))
ADMINS = str(os.getenv('ADMINS'))
DB_LINK = str(os.getenv('DB_LINK'))


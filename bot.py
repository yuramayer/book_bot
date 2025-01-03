import logging
from config import conf
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(
    token=conf.BOT_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


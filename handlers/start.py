from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

start_router = Router()

@start_router.message(Command('test'))
async def cmd_start(message: Message):
    await message.answer('Привет!\n\nЗдесь будет бот по чтению 📘')

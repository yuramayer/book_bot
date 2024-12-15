from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from filters.admin_checker import IsAdmin
from config.conf import admins_ids, books
from keyboards.first_keyboard import get_book_choice


start_router = Router()
start_router.message.filter(
    IsAdmin(admins_ids)
)

@start_router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Привет!\n\nЗдесь будет бот по чтению 📘')
    await message.answer('Выбери книгу', reply_markup=get_book_choice())


@start_router.message(F.text.in_(books))
async def book_choice(message: Message):
    await message.answer(f'Хороший выбор: {message.text}')



@start_router.message(F.text.lower() == 'кек')
async def test(message: Message):
    await message.answer('КЕК!')

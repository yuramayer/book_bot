from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from filters.admin_checker import IsAdmin
from config.conf import admins_ids, books
from keyboards.first_keyboard import get_book_choice
from back.db_back import get_last_book, update_last_book

start_router = Router()
start_router.message.filter(
    IsAdmin(admins_ids)
)

@start_router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Привет!\n\nЗдесь будет бот по чтению 📘')
    last_book_tpl = get_last_book(message.chat.id)
    if last_book_tpl:
        last_book, = last_book_tpl
        await message.answer(f'У тебя уже есть книга: {last_book}')
    else:
        await message.answer('Выбери книгу', reply_markup=get_book_choice())


@start_router.message(F.text.in_(books))
async def book_choice(message: Message):
    update_last_book(message.chat.id, message.text)
    await message.answer(f'Хороший выбор: {message.text}')



@start_router.message(F.text.lower() == 'кек')
async def test(message: Message):
    await message.answer('КЕК!')

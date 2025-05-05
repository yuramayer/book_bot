"""Bot reacts to the new book from user"""

from aiogram import Router, F
from aiogram.types import Message
from filters.admin_checker import IsAdmin
from config.conf import admins_ids, books
from back.db_back import update_last_book
from back.cache import BOOK_DICT, BOOK_CACHE, load_book
from keyboards.page_keyboard import change_page

choice_router = Router()
choice_router.message.filter(
    IsAdmin(admins_ids)
)


@choice_router.message(F.text.in_(books.keys()))
async def book_choice(message: Message):
    """User choose book & bot download it"""
    update_last_book(message.chat.id, message.text)
    BOOK_CACHE[message.chat.id] = message.text
    load_book(message.text, BOOK_DICT)
    await message.answer(
        f'Хороший выбор: {message.text}', reply_markup=change_page())

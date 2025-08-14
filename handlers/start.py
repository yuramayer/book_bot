"""Bot reacts to the command /start"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from keyboards.book_keyboard import get_book_choice
from back.db_back import get_last_book
from back.cache import BOOK_CACHE, BOOK_DICT, load_book


start_router = Router()
start_router.message.filter(
    IsAdmin(admins_ids)
)


@start_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """User starts bot, and bot asks user about the book"""
    await state.clear()
    last_book_tpl = get_last_book(message.chat.id)

    if not last_book_tpl:
        await message.answer('Какую книгу будем читать?',
                             reply_markup=get_book_choice())
        return

    last_book, = last_book_tpl
    BOOK_CACHE[message.chat.id] = last_book
    load_book(last_book, BOOK_DICT)
    await message.answer(
        f'У тебя уже есть книга: <b>{last_book}</b>')
    msg = 'Нажми 👉 <b>/read</b> чтобы вернуться к чтению'
    await message.answer(msg)

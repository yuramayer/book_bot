"""Bot reacts to the button <left page>"""

from aiogram import Router, F
from aiogram.types import Message
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from back.cache import BOOK_DICT, BOOK_CACHE
from back.db_back import get_page_from_db, update_page_db
from back.bot_back import prettify_text
from keyboards.page_keyboard import change_page
from keyboards.book_keyboard import get_book_choice

left_router = Router()
left_router.message.filter(
    IsAdmin(admins_ids)
)


@left_router.message(F.text == '⬅️')
async def prev_page(message: Message):
    """User wants the previous page, bot downloads it and sends"""
    book = BOOK_CACHE.get(message.chat.id)
    if not book:
        await message.answer('Выбери книгу', reply_markup=get_book_choice())
        return

    loaded_book = BOOK_DICT.get(book)
    if not loaded_book:
        await message.answer('Книга не загружена')
        return

    current_page_tpl = get_page_from_db(message.chat.id, book)
    if not current_page_tpl:
        await message.answer("You don't have the current page for the book")
        await message.answer("The book is started for you ☺️")
        return

    current_page, = current_page_tpl
    current_page = str(current_page - 1)

    page_text = loaded_book.get(current_page)
    if not page_text:
        await message.answer('Такой страницы в книге нет')
        return

    update_page_db(message.chat.id, book, current_page)

    pretty_page_text = prettify_text(current_page, page_text)

    await message.answer(pretty_page_text, reply_markup=change_page())

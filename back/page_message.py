"""Template for sending the page of the book"""

from aiogram.types import Message
from keyboards.page_keyboard import change_page
from keyboards.book_keyboard import get_book_choice
from back.cache import BOOK_CACHE, BOOK_DICT
from back.db_back import get_page_from_db, update_page_db, start_book
from back.bot_back import prettify_text


async def create_and_send_page(message: Message, _type=None):
    """Gets page and sends it to the user"""
    book = BOOK_CACHE.get(message.chat.id)
    if not book:
        await message.answer('Какую книгу будем читать? 📘',
                             reply_markup=get_book_choice())
        return

    loaded_book = BOOK_DICT.get(
        book)
    if not loaded_book:
        await message.answer('Книга не загружена')
        return

    current_page_tpl = get_page_from_db(message.chat.id, book)
    if not current_page_tpl:
        await message.answer("You don't have the current page for the book")
        start_book(book, message.chat.id)
        await message.answer("The book is started for you ☺️")
        return

    current_page, = current_page_tpl
    if _type == 'left':
        current_page = str(current_page - 1)
    elif _type == 'right':
        current_page = str(current_page + 1)
    else:
        current_page = str(current_page)

    page_text = loaded_book.get(current_page)
    if not page_text:
        await message.answer('Такой страницы в книге нет 🥺')
        return

    update_page_db(message.chat.id, book, current_page)

    pretty_page_text = prettify_text(current_page, page_text)

    await message.answer(pretty_page_text, reply_markup=change_page())

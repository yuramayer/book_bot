from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config.conf import books

def get_book_choice() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for book in books.keys():
        kb.button(text=book)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
 
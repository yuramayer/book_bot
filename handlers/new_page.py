"""Changing the page of the book with the bot"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from filters.admin_checker import IsAdmin
from config.conf import admins_ids, books
from keyboards.book_keyboard import get_book_choice
from states import NewPage
from back.bot_back import is_positive, is_page_in_book
from back.db_back import set_new_page


new_page_router = Router()
new_page_router.message.filter(
    IsAdmin(admins_ids)
)


@new_page_router.message(Command('new_page'))
async def cmd_new_page(message: Message, state: FSMContext):
    """User choose book to change the page"""
    msg1 = 'В какой книге поменяем страницу? 🤔'
    msg2 = 'Выбери книгу с помощью клавиатуры ниже:'
    await message.answer(f'{msg1}\n\n{msg2}',
                         reply_markup=get_book_choice())
    await state.set_state(NewPage.book)


@new_page_router.message(NewPage.book, F.text.in_(books.keys()))
async def ask_page(message: Message, state: FSMContext):
    """Bot asks user the page to change"""
    await state.update_data(book=message.text)
    msg = "Отправь новую страницу для книги, только цифру"
    await message.answer(msg,
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewPage.new_page)


@new_page_router.message(NewPage.book)
async def wrong_book(message: Message):
    """Bot asks user to send correct book"""
    msg1 = 'Я не знаю такой книги 😿'
    msg2 = 'Пожалуйста, выбери книгу с помощью специальной клавиатуры:'
    await message.answer(f'{msg1}\n\n{msg2}',
                         reply_markup=get_book_choice())


@new_page_router.message(NewPage.new_page)
async def check_and_save_page(message: Message, state: FSMContext):
    """Bot checks new page for the book & save it to the DB"""
    users_page = message.text
    if not is_positive(users_page):
        msg = 'Пожалуйста, отправь новую страницу виде числа 🙏🏻'
        await message.answer(msg)
        await state.set_state(NewPage.new_page)
        return

    book = await state.get_value('book')

    if not is_page_in_book(users_page, book):
        msg1 = 'В книге нет такой страницы! 😰'
        msg2 = 'Пожалуйста, отправь нормальную новую страницу в виде числа'
        await message.answer(f'{msg1}\n\n{msg2}')
        await state.set_state(NewPage.new_page)
        return

    await state.update_data(new_page=users_page)

    new_page_dict = await state.get_data()

    set_new_page(new_page_dict.get('book'), new_page_dict.get('new_page'),
                 message.chat.id)

    bk = new_page_dict.get("book")
    pg = new_page_dict.get("new_page")
    msg1 = 'Готово 👌🏻'
    msg2 = f'Новая страница для книги "{bk}" - {pg}'
    await message.answer(f'{msg1}\n\n{msg2}',
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await message.answer('Нажми <b>/read</b> чтобы вернуться к чтению')

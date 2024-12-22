from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from filters.admin_checker import IsAdmin
from config.conf import admins_ids, books
from keyboards.book_keyboard import get_book_choice
from keyboards.page_keyboard import change_page
from back.db_back import get_last_book, update_last_book, get_page_from_db, update_page_db
from back.cache import BOOK_CACHE, BOOK_DICT, load_book, add_newlines


start_router = Router()
start_router.message.filter(
    IsAdmin(admins_ids)
)


@start_router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Привет!\n\nЗдесь будет бот по чтению 📘')
    last_book_tpl = get_last_book(message.chat.id)
    
    if not last_book_tpl:
        await message.answer('Выбери книгу', reply_markup=get_book_choice())
        return 
    
    last_book, = last_book_tpl 
    BOOK_CACHE[message.chat.id] = last_book
    load_book(last_book, BOOK_DICT)
    await message.answer(f'У тебя уже есть книга: {last_book}', reply_markup=change_page())
    
    

@start_router.message(F.text.in_(books.keys()))
async def book_choice(message: Message):
    update_last_book(message.chat.id, message.text)
    load_book(message.text, BOOK_DICT)
    BOOK_CACHE[message.chat.id] = message.text
    await message.answer(f'Хороший выбор: {message.text}', reply_markup=change_page())



@start_router.message(F.text == '⬅️')
async def prev_page(message: Message):
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
        await message.answer('Страница не найдена в БД')
        return
    
    current_page, = current_page_tpl
    current_page = str(current_page - 1) 

    page_text = loaded_book.get(current_page)
    if not page_text:
        await message.answer('Такой страницы в книге нет')
        return 
    
    update_page_db(message.chat.id, book, current_page)
    
    await message.answer(page_text, reply_markup=change_page())



@start_router.message(F.text == '➡️')
async def next_page(message: Message):
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
        await message.answer('Страница не найдена в БД')
        return
    
    current_page, = current_page_tpl
    current_page = str(current_page + 1) 

    page_text = loaded_book.get(current_page)
    if not page_text:
        await message.answer('Такой страницы в книге нет')
        return 
    
    update_page_db(message.chat.id, book, current_page)
    
    page_text = add_newlines(page_text)

    await message.answer(page_text, reply_markup=change_page())


@start_router.message(F.text.lower() == 'кек')
async def test(message: Message):
    await message.answer('КЕК!', reply_markup=ReplyKeyboardRemove())

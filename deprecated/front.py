from config import TEST_BOT_TOKEN, REAL_BOT_TOKEN, BOOK_LIST, ADMIN_DICT
from back.db_back import get_page_from_db, update_page_db
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.utils.emoji import emojize
from typing import Tuple, List
from collections import namedtuple
import json
from nltk import tokenize
from googletrans import Translator


Reader = namedtuple('Reader', ['step', 'book', 'page'])
reader_dict = {}
book_dict = {}


@dp.message_handler(commands=['start'])
async def first_message(message: types.Message):

    async def f(message: types.Message):

        update_reader(message.chat.id, 1)
        msg = await get_first_message(message.chat.id)
        keyboard = await get_first_keyboard()
        await message.answer(msg, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

    await wrapper(message, f, step=None)


@dp.message_handler(lambda message: message.text in BOOK_LIST)
async def ask_page(message: types.Message):

    async def f(message: types.Message):

        reader_params = get_reader_params(message.chat.id)
        reader_params[0] = 2
        update_reader(message.chat.id, *reader_params, message.text)

        create_book_dict(message.text)

        msg = await get_ask_message(message.chat.id)
        keyboard = await get_ask_keyboard()
        await message.answer(msg, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

    await wrapper(message, f, step=1)


@dp.message_handler(Text(equals='Yes, let\'s read'))
async def send_first_page(message: types.Message, is_change_page=False):

    async def f(message: types.Message):

        reader_params = get_reader_params(message.chat.id)
        reader_params[0] = 4

        reader = ADMIN_DICT[message.chat.id]
        title = reader_dict[message.chat.id].book
        page = get_page_from_db(reader, title)
        if is_change_page:
            update_reader(message.chat.id, *reader_params)
        else:
            update_reader(message.chat.id, *reader_params, page)
        msg = await get_next_page(message.chat.id)
        keyboard = await get_page_keyboard()

        await message.answer(msg, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

    step = 4 if is_change_page else 2

    await wrapper(message, f, step=step)


@dp.message_handler(Text(equals='Change page'))
async def ask_page_number(message: types.Message):

    async def f(message: types.Message):

        reader_params = get_reader_params(message.chat.id)
        reader_params[0] = 3
        update_reader(message.chat.id, *reader_params)

        await message.answer('Send me the page number as integer')

    await wrapper(message, f, step=2)


@dp.message_handler(lambda message: message.text.isdigit())
async def update_page_number(message: types.Message):

    async def f(message: types.Message):
        reader_params = get_reader_params(message.chat.id)
        reader_params[0] = 4
        update_reader(message.chat.id, *reader_params, page=int(message.text))
        await send_first_page(message, is_change_page=True)


    await wrapper(message, f, step=3)


@dp.message_handler(Text(equals='➡️'))
async def send_next_page(message: types.Message):

    async def f(message: types.Message):
        new_page = reader_dict[message.chat.id].page + 1
        reader_params = get_reader_params(message.chat.id)
        reader_params[2] = new_page
        update_reader(message.chat.id, *reader_params)

        await get_params_and_update_db(message.chat.id, new_page)

        msg = await get_next_page(message.chat.id)
        keyboard = await get_page_keyboard()
        await message.answer(msg, parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


    await wrapper(message, f, step=4)


@dp.message_handler(Text(equals='⬅️'))
async def send_prev_page(message: types.Message):

    async def f(message: types.Message):
        new_page = reader_dict[message.chat.id].page - 1
        reader_params = get_reader_params(message.chat.id)
        reader_params[2] = new_page
        update_reader(message.chat.id, *reader_params)

        await get_params_and_update_db(message.chat.id, new_page)

        msg = await get_next_page(message.chat.id)
        keyboard = await get_page_keyboard()
        await message.answer(msg, parse_mode=types.ParseMode.HTML, reply_markup=keyboard)

    await wrapper(message, f, step=4)


@dp.message_handler()
async def translate_message(message: types.Message):

    translator = Translator()
    translation = translator.translate(message.text, dest='ru', src='en').text
    await message.answer(f'👉🏻 <i>{message.text} - <b>{translation}</b></i>', parse_mode=types.ParseMode.HTML)


async def wrapper(message: types.Message, f, step: int):
    """Check if function should be called. Takes Message obj, function & user step"""
    if await is_not_admin(message.chat.id):
        await message.answer('Error: You are not admin 😥\n\nAny questions: @botrqst')


    elif await is_bad_page(message.chat.id, message.text, step):
        await message.answer('Error: there is no such page in this book 😥\n\nType me another page:')


    elif await is_wrong_way(message.chat.id, step):
        await message.answer('Error: Wrong Type 😥'
                             '\n\nPlease, start again: /start')


    elif await is_ended_book(message.chat.id, message.text, step):
        keyboard = await get_page_keyboard()
        await message.answer('Notion: The book is ended here!', reply_markup=keyboard)
    else:
        await f(message)


async def is_wrong_way(chat_id: int, step: int) -> bool:
    """Returns True if user sends something wrong. Takes message.chat.id & user step"""
    if step:
        if chat_id not in reader_dict:
            return True
        reader_step = reader_dict[chat_id].step
        if step != reader_step:
            return True


async def is_not_admin(chat_id: int) -> bool:
    """Returns True if message.chat.id is missing in ADMIN DICT"""
    if chat_id not in ADMIN_DICT:
        return True


async def is_bad_page(chat_id: int, text: str, step: int) -> bool:
    """Returns True if page is missing in the book"""
    if step == 3:
        if not text.isdigit():
            return True
        title = reader_dict[chat_id].book
        l = len(book_dict[title])
        page = int(text)
        if (page < 0) or (page >= l):
            return True




async def is_ended_book(chat_id: int, text: str, step: int) -> bool:
    """Returns True if new_page not in (0, len(book))"""
    if step == 4:
        page = reader_dict[chat_id].page
        if text == '⬅️':
            page -= 1
        elif text == '➡️':
            page += 1
        title = reader_dict[chat_id].book
        l = len(book_dict[title])
        if (page < 0) or (page >= l):
            return True


async def get_first_message(chat_id) -> str:
    """Returns first message text. Takes message.chat.id"""
    txt = f"Hello, {ADMIN_DICT[chat_id]}! 🙋🏼‍♀️\n\nWould you like to read?"
    return txt


async def get_first_keyboard() -> types.ReplyKeyboardMarkup:
    """Returns first message keyboard with books"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*BOOK_LIST)
    return keyboard


def create_book_dict(book: str):
    """Loads book to book_dict[BOOK_NAME]. Format: {index: sentence}"""
    with open(f'{book}.json', 'r') as my_book:
        book_json = my_book.read()

    book_dict[f'{book}'] = json.loads(book_json)


async def get_ask_message(chat_id) -> str:
    """Returns page question text"""
    reader = ADMIN_DICT[chat_id]
    title = reader_dict[chat_id].book
    page = get_page_from_db(reader, title)
    txt = f"Your page is {page}, isn\'t it?"
    return txt


async def get_ask_keyboard() -> types.ReplyKeyboardMarkup:
    """Returns page question keyboard with 'Yes, let's read'"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add('Yes, let\'s read', 'Change page')
    return keyboard


async def get_next_page(chat_id) -> str:
    """Returns book page text. Takes message.chat.id"""
    page = str(reader_dict[chat_id].page)
    title = reader_dict[chat_id].book
    book = book_dict[title]
    text = book[page] if page in book else 'Null'
    txt = f'📖 <b>page {page}</b>\n\n'
    txt += '\n\n'.join(tokenize.sent_tokenize(text))

    return txt


async def get_page_keyboard() -> types.ReplyKeyboardMarkup:
    """Returns keyboard with arrows: left & right"""
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add('⬅️', '➡️')
    return keyboard


async def get_params_and_update_db(chat_id: int, page: int):
    """Gets reader name, book title; Update page in database"""
    reader = ADMIN_DICT[chat_id]
    title = reader_dict[chat_id].book
    update_page_db(reader, title, page)


def get_reader_params(reader_id) -> List:
    """Returns Reader obj. attributes: step, book, page. Takes message.chat.id"""
    reader_params = list(i for i in reader_dict[reader_id] if i is not None)
    return reader_params


def update_reader(reader_id, step=None, book=None, page=None, delete=False):
    """Updates Reader namedtuple in reader_dict. Takes message.chat.id & Reader attributes"""
    reader_dict[reader_id] = Reader(step=step, book=book, page=page)
    if delete:
        del reader_dict[reader_id]






if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, )
    except Exception as e:
        pass


"""Cache for the bot"""

import json 
from config.conf import books

BOOK_CACHE = {}
BOOK_DICT = {}


def load_book(book_title: str, book_dict: dict):
    """Loading the json-book into the cache dict"""

    book_path = books.get(book_title)
    if not book_path:
        print("The book wasn't found")
        return

    with open(book_path, 'r', encoding='utf-8') as book:
        book_json = book.read()

    book_dict[book_title] = json.loads(book_json)

from config.conf import books
import json 

BOOK_CACHE = {}
BOOK_DICT = {}

print('ПОДКЛЮЧАЕМ КЭШ!!!!')


def load_book(book_title, book_dict):
    book_path = books.get(book_title)
    if not book_path:
        print('Книга не найдена') 
        return
    with open(book_path, 'r') as book:
        book_json = book.read()

    book_dict[book_title] = json.loads(book_json)

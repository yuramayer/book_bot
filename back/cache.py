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


def add_newlines(text):
    text = text.replace('\n', ' ')

    result = ""
    punctuation = {'.', '!', '?', ';', ':', '...'} 

    i = 0
    while i < len(text):
        result += text[i]
        if text[i] in punctuation:
            if i + 1 < len(text) and text[i + 1] == ' ':
                result += "\n\n"
        i += 1
    
    result = result.replace('\n ', '\n')

    return result

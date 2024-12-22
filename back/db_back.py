import sqlite3
import sys
from typing import Tuple
from config.conf import DB_LINK


def check_db():
    """Check if database is in the catalogue"""
    try:
        sqlite_con = sqlite3.connect(DB_LINK)
        cursor = sqlite_con.cursor()
        print('DB is successfully connected')
        cursor.close()

    except sqlite3.Error as error:
        print(f'Error w/ connecting to the {DB_LINK}:', error)
        sys.exit()

    finally:
        if sqlite_con:
            sqlite_con.close()


check_db()


def get_last_book(reader: str) -> tuple | None:
    """Returns user's last book in tuple. If there's no any book - returns None"""
    sqlite_con = sqlite3.connect(DB_LINK)
    cursor = sqlite_con.cursor()

    query = "SELECT book FROM current_books WHERE (reader = ?)"
    last_book_tpl = cursor.execute(query, (reader,)).fetchone()

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()

    return last_book_tpl


def update_last_book(reader: str, book: str):
    """Updates user's last book"""
    sqlite_con = sqlite3.connect(DB_LINK)
    cursor = sqlite_con.cursor()
    
    query = "DELETE FROM current_books WHERE (reader = ?) AND (book = ?)"
    cursor.execute(query, (reader, book))

    query = "INSERT INTO current_books (reader, book) VALUES (?, ?)"
    cursor.execute(query, (reader, book))

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()


def get_page_from_db(reader: int, book: str) -> int | None:
    """Returns page from database. Takes reader & book"""
    sqlite_con = sqlite3.connect(DB_LINK)
    cursor = sqlite_con.cursor()

    query = "SELECT page FROM books_table WHERE (reader = ?) AND (book = ?)"
    page_tpl = cursor.execute(query, (reader, book)).fetchone()
    
    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()

    return page_tpl


def update_page_db(reader: int, book: str, new_page: int):
    """Updates database with new page. Takes reader, book & new page"""
    sqlite_con = sqlite3.connect(DB_LINK)
    cursor = sqlite_con.cursor()

    query = "DELETE FROM books_table WHERE (reader = ?) AND (book = ?)"
    cursor.execute(query, (reader, book))

    query = "INSERT INTO books_table (reader, book, page) VALUES (?, ?, ?)"
    cursor.execute(query, (reader, book, new_page))

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()

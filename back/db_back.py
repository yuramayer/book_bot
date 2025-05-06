"""Methods for the sqlite database"""

import sqlite3
import os
from config.conf import DB_PATH


async def is_checked_db():
    """Check if database is in the catalogue"""
    try:
        sqlite_con = sqlite3.connect(DB_PATH)
        cursor = sqlite_con.cursor()
        cursor.close()

    except sqlite3.Error as error:
        print(f'Error w/ connecting to the {DB_PATH}:', error)
        return False

    finally:
        if sqlite_con:
            sqlite_con.close()

    return True


def get_last_book(reader: str) -> tuple | None:
    """Returns user's last book in tuple.
    If there's no any book - returns None"""
    sqlite_con = sqlite3.connect(DB_PATH)
    cursor = sqlite_con.cursor()

    query = "SELECT book FROM current_books WHERE (reader = ?)"
    last_book_tpl = cursor.execute(query, (reader,)).fetchone()

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()

    return last_book_tpl


def update_last_book(reader: str, book: str):
    """Updates user's last book"""
    sqlite_con = sqlite3.connect(DB_PATH)
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
    sqlite_con = sqlite3.connect(DB_PATH)
    cursor = sqlite_con.cursor()

    query = "SELECT page FROM books_table WHERE (reader = ?) AND (book = ?)"
    page_tpl = cursor.execute(query, (reader, book)).fetchone()

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()

    return page_tpl


def update_page_db(reader: int, book: str, new_page: int):
    """Updates database with new page. Takes reader, book & new page"""
    sqlite_con = sqlite3.connect(DB_PATH)
    cursor = sqlite_con.cursor()

    query = "DELETE FROM books_table WHERE (reader = ?) AND (book = ?)"
    cursor.execute(query, (reader, book))

    query = "INSERT INTO books_table (reader, book, page) VALUES (?, ?, ?)"
    cursor.execute(query, (reader, book, new_page))

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()


def create_books_database():
    """Creates the database if it doesn't exist"""

    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        print("The database wasn't found and was created successfully")
        sqlite_con = sqlite3.connect(DB_PATH)
        sqlite_con.close()
    else:
        print("The database was found")


def create_books_table():
    """Creates the table with books if it doesn't exist"""

    sqlite_con = sqlite3.connect(DB_PATH)
    cursor = sqlite_con.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='books_table';
    """)

    table_exists = cursor.fetchone()

    if table_exists:
        print("The table 'books_table' was found")
        return

    cursor.execute("""
        CREATE TABLE 'books_table' (
            book TEXT,
            reader INTEGER,
            page INTEGER
        );
    """)
    print("The table 'books_table' wasn't found and was created successfully")

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()


def create_current_books_table():
    """Creates the table with current books for readers if it doesn't exist"""

    sqlite_con = sqlite3.connect(DB_PATH)
    cursor = sqlite_con.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='current_books';
    """)

    table_exists = cursor.fetchone()

    if table_exists:
        print("The table 'current_books' was found")
        return

    cursor.execute("""
        CREATE TABLE current_books (
            reader INTEGER,
            book TEXT
        );
    """)
    print("The table 'current_books' wasn't found \
          and was created successfully")

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()


def start_book(book_name: str, user_id: int):
    """Creates the book for the user with the page 0"""

    sqlite_con = sqlite3.connect(DB_PATH)
    cursor = sqlite_con.cursor()

    query = """
        INSERT INTO books_table
        VALUES (?, ?, 0)
    """
    cursor.execute(query, (book_name, user_id))

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()


def set_new_page(book_name: str, new_page: int, user_id: int):
    """Set new page for the book in the 'books_table'"""

    sqlite_con = sqlite3.connect(DB_PATH)
    cursor = sqlite_con.cursor()

    query = """
        UPDATE books_table
        SET page = ?
        WHERE 1=1
        AND (reader = ?)
        AND (book = ?)
        ;
    """
    cursor.execute(query, (new_page, user_id, book_name))

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()

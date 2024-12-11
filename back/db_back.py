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


def get_page_from_db(reader: str, book: str) -> int:
    """Returns page from database. Takes reader & book"""
    sqlite_con = sqlite3.connect(DB_LINK)
    cursor = sqlite_con.cursor()

    query = "SELECT Page FROM book WHERE (Reader = ?) AND (Book = ?)"

    res_tuple = cursor.execute(query, (reader, book)).fetchone()
    page = res_tuple[0]

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()

    return page


def update_page_db(reader: str, book: str, page: int):
    """Updates database with new page. Takes reader, book & page"""
    sqlite_con = sqlite3.connect(DB_LINK)
    cursor = sqlite_con.cursor()

    query = "UPDATE book SET Page = ? WHERE (Reader = ?) AND (Book = ?)"

    cursor.execute(query, (page, reader, book))

    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()

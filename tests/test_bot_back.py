import os
import sqlite3
import importlib
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def _reload_bot_back(db_path: str, monkeypatch) -> "module":
    # Set required environment variables for config
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("OPENAI_TOKEN", "token")
    monkeypatch.setenv("ADMINS", "1")
    monkeypatch.setenv("BOOKS", "TestBook")
    monkeypatch.setenv("BOOKS_PATH", "test.json")
    monkeypatch.setenv("DB_PATH", db_path)

    import config.conf
    import back.db_back
    import back.bot_back

    importlib.reload(config.conf)
    importlib.reload(back.db_back)
    return importlib.reload(back.bot_back)


@pytest.fixture
def bot_back(tmp_path, monkeypatch):
    db_path = tmp_path / "books.db"
    bot_back = _reload_bot_back(str(db_path), monkeypatch)

    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE books_length (book text, len integer);")
    conn.execute(
        "INSERT INTO books_length (book, len) VALUES (?, ?)",
        ("TestBook", 5),
    )
    conn.commit()
    conn.close()
    return bot_back


@pytest.mark.parametrize(
    "value, expected",
    [
        ("10", True),
        ("0", False),
        ("-1", False),
        ("abc", False),
    ],
)
def test_is_positive(bot_back, value, expected):
    assert bot_back.is_positive(value) is expected


def test_page_in_range(bot_back):
    assert bot_back.is_page_in_book("3", "TestBook") is True


def test_page_out_of_range(bot_back):
    assert bot_back.is_page_in_book("6", "TestBook") is False


def test_page_no_book(bot_back):
    assert bot_back.is_page_in_book("1", "Unknown") is False

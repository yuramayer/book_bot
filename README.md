# 📘 Telegram English Reading Bot

Telegram bot built with **aiogram** that helps you read books & translate words using **GPT**

## 🤖 Bot Commands

| Command        | Description                    |
|----------------|--------------------------------|
| `/read`        | Show current book page         |
| `/new_page`    | Jump to the different page     |
| `/change_book` | Switch to another book         |
| `/cancel`      | Stop the current operation     |

You can also use the arrow buttons (`➡️`, `⬅️`) to navigate pages

Any phrase you send will be automatically translated using ChatGPT


## 🛠️ How to Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up your configs**:
    
    Create a `.env` file in the project root with the following variables:

    ```env
    BOT_TOKEN=your_telegram_bot_token
    OPENAI_TOKEN=your_openai_api_key
    ADMINS=123456789,987654321              # TG admins, comma-separated
    BOOKS=English Book;Russian Book         # book names, ;-separated
    BOOKS_PATH=books/en.txt;books/ru.txt    # paths to books, ;-separated
    DB_PATH=database/books_database.db                 # path to sqlite database
    ```
    - `BOOKS` & `BOOKS_PATH` must match in length and order — each book name maps to its json-file
    - `ADMINS` will receive admin access to bot commands
    - ❗️ If any variable is missin, the bot'll raise an error at startup

3. **Run the bot**:
    ```bash
    python app.py
    ```
4. **Deploy on the server** with systemd for background running ✨

## 💬 Powered by

[![aiogram](https://img.shields.io/badge/aiogram-v3-blue?logo=telegram)](https://docs.aiogram.dev/en/latest/)
[![python-dotenv](https://img.shields.io/badge/dotenv-.env-green?logo=python)](https://github.com/theskumar/python-dotenv)
[![OpenAI](https://img.shields.io/badge/OpenAI-ChatGPT-black?logo=openai)](https://platform.openai.com/docs)
[![systemd](https://img.shields.io/badge/systemd-Linux-blue?logo=linux)](https://www.freedesktop.org/wiki/Software/systemd/)

- **[aiogram 3](https://github.com/aiogram/aiogram)**
- **[OpenAI GPT API](https://platform.openai.com/docs)**

----

Need help? Open an issue 😉

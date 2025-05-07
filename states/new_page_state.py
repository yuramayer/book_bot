"""State for the book's page updating"""

# pylint: disable=too-few-public-methods

from aiogram.fsm.state import StatesGroup, State


class NewPage(StatesGroup):
    """New page State: saves book & new page"""
    book = State()
    new_page = State()

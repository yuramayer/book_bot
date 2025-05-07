"""Bot reacts to the command /change_book"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from keyboards.book_keyboard import get_book_choice


change_book_router = Router()
change_book_router.message.filter(
    IsAdmin(admins_ids)
)


@change_book_router.message(Command('change_book'))
async def cmd_change_booko(message: Message):
    """User asks bot to change the current book"""

    await message.answer('Выбери книгу', reply_markup=get_book_choice())

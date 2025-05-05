"""Message for all the other users - not admins"""

from aiogram import Router, F
from aiogram.types import Message
from filters.admin_checker import NotAdmin
from config.conf import admins_ids


dummy_router = Router()
dummy_router.message.filter(
    NotAdmin(admins_ids)
)


@dummy_router.message(F.text)
async def dummy(message: Message):
    """User - not admin tries to talk with the bot"""
    await message.answer('Бот доступен для администраторов 🥲\n\n'
                         'Вопросы: <b>@botrqst</b>')

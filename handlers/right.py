"""Bot reacts to the button <right page>"""

from aiogram import Router, F
from aiogram.types import Message
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from back.page_message import create_and_send_page


right_router = Router()
right_router.message.filter(
    IsAdmin(admins_ids)
)


@right_router.message(F.text == '➡️')
async def next_page(message: Message):
    """User wants the next page, bot downloads it and sends"""
    await create_and_send_page(message, 'right')

"""Bot reacts to the button <left page>"""

from aiogram import Router, F
from aiogram.types import Message
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from back.page_message import create_and_send_page


left_router = Router()
left_router.message.filter(
    IsAdmin(admins_ids)
)


@left_router.message(F.text == '⬅️')
async def prev_page(message: Message):
    """User wants the previous page, bot downloads it and sends"""
    await create_and_send_page(message, _type='left')

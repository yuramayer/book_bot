"""Bot sends current page"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from back.page_message import create_and_send_page


read_page_router = Router()
read_page_router.message.filter(
    IsAdmin(admins_ids)
)


@read_page_router.message(Command('read'))
async def cmd_read(message: Message, state: FSMContext):
    """Sends current page to the user"""
    await state.clear()
    await create_and_send_page(message)

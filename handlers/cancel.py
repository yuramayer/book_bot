"""Clear the FSM cache"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from filters.admin_checker import IsAdmin
from config.conf import admins_ids


cancel_router = Router()
cancel_router.message.filter(
    IsAdmin(admins_ids)
)


@cancel_router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    """User wants to clear the FSM cache"""
    await state.clear()
    msg1 = 'Операция отменена 🤝'
    msg2 = 'Нажми <b>/read</b> чтобы вернуться к чтению'
    await message.answer(f'{msg1}\n\n{msg2}',
                         reply_markup=ReplyKeyboardRemove())

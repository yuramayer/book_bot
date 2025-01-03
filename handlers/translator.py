from aiogram import Router, F
from aiogram.types import Message
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from back.bot_back import translate_word
from keyboards.page_keyboard import change_page


translation_router = Router()
translation_router.message.filter(
    IsAdmin(admins_ids)
)


@translation_router.message(F.text)
async def translate(message: Message):
    translation = translate_word(message.text)
    await message.answer(translation, reply_markup=change_page())

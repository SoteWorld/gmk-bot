from aiogram import Router, F
from aiogram.types import Message

from ..keyboards import menu_markup

router = Router(name="fallback")

@router.message(F.text)
async def unknown_message(message: Message) -> None:
    await message.answer(
        "Извините, не понял сообщение. Используйте /menu для выбора действия.",
        reply_markup=menu_markup,
    )
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..keyboards import menu_markup

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=menu_markup,
    )
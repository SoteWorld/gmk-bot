from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from ..keyboards import menu_markup

router = Router(name="start")


@router.message(Command("start", "menu"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=menu_markup,
    )


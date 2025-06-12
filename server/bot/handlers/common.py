from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..keyboards import main_markup

router = Router(name="common")

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Hello, world!", reply_markup=main_markup)
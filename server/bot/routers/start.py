from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from ..keyboards import menu_markup

router = Router(name="start")


@router.message(Command("start", "menu"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "✨ Добро пожаловать!\n📋 Выберите действие:",
        reply_markup=menu_markup,
    )


@router.callback_query(F.data == "menu")
async def menu_callback(call: CallbackQuery) -> None:
    await call.message.edit_text(
        "✨ Добро пожаловать!\n📋 Выберите действие:",
        reply_markup=menu_markup,
    )
    await call.answer()
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from ..keyboards import menu_markup

router = Router(name="help")

HELP_TEXT = (
    "Этот бот помогает узнать о новых продуктах и найти ближайший магазин.\n\n"
    "Команды:\n"
    "/menu - открыть меню\n"
    "/help - справка"
)

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=menu_markup)


@router.callback_query(F.data == "help")
async def help_callback(call: CallbackQuery) -> None:
    await call.message.answer(HELP_TEXT, reply_markup=menu_markup)
    await call.answer()
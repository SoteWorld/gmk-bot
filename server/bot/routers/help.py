from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from ..keyboards import help_markup


router = Router(name="help")

HELP_TEXT = (
    "🤖 Я помогу вам следить за новинками нашей продукции и подскажу, где находится ближайший магазин.\n\n"
    "📌 Основные команды:\n"
    "👉 /menu - открыть главное меню\n"
    "👉 /help - показать эту справку\n"
    "Если возникли вопросы, смело обращайтесь!"
)

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=help_markup)


@router.callback_query(F.data == "help")
async def help_callback(call: CallbackQuery) -> None:
    await call.message.edit_text(HELP_TEXT, reply_markup=help_markup)
    await call.answer()

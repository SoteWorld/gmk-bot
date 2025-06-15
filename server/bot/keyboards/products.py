from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def product_nav_markup(index: int, total: int) -> InlineKeyboardMarkup:
    """Клавиатура навигации по продуктам."""
    builder = InlineKeyboardBuilder()
    if index > 0:
        builder.button(text="⬅️ Назад", callback_data=f"product:{index - 1}")
    builder.button(text="В меню", callback_data="menu")
    if index < total - 1:
        builder.button(text="Вперёд ➡️", callback_data=f"product:{index + 1}")
    builder.adjust(3)
    return builder.as_markup()
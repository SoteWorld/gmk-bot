from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from server.config_reader import config

# Main menu with all available actions
menu_builder = InlineKeyboardBuilder()
menu_builder.button(text="Наши продукты", callback_data="products")
menu_builder.button(text="📍 Магазины рядом", callback_data="stores")
menu_builder.button(
    text="🌐 Открыть Mini App", web_app=WebAppInfo(url=config.WEBAPP_URL)
)
menu_builder.button(text="ℹ️ Помощь", callback_data="help")
menu_builder.adjust(1)

menu_markup = menu_builder.as_markup()

# Keyboard for the help command – only menu and Mini App buttons
help_builder = InlineKeyboardBuilder()
help_builder.button(
    text="🌐 Открыть Mini App", web_app=WebAppInfo(url=config.WEBAPP_URL)
)
help_builder.button(text="🏠 Главное Меню", callback_data="menu")

help_builder.adjust(1)

help_markup = help_builder.as_markup()

from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from server.config_reader import config

builder = InlineKeyboardBuilder()
builder.button(text="Новые продукты", callback_data="products")
builder.button(text="Ближайшие магазины", callback_data="stores")
builder.button(text="Открыть Mini App", web_app=WebAppInfo(url=config.WEBAPP_URL))
builder.adjust(1)

menu_markup = builder.as_markup()
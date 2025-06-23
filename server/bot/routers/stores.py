from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from server.services.data_provider import DataProvider
from ..keyboards import menu_markup

router = Router(name="stores")
provider = DataProvider()

location_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📍 Отправить локацию", request_location=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


@router.callback_query(F.data == "stores")
async def request_location(call: CallbackQuery) -> None:
    await call.message.answer(
        "📍 Отправьте свою геолокацию",
        reply_markup=location_keyboard,
    )
    await call.answer()

ITEMS_PER_PAGE = 5

def build_page_text(stores, start, end):
    parts = []
    for store in stores[start:end]:
        part = (
            f"🏬 <b>{store.name}</b>\n"
            f"📬 Адрес: {store.address}\n"
            f"🗺️ Расстояние: {store.distance:.1f} км"
        )
        if store.opening_hours:
            part += f"\n⌛️ Время работы: {store.opening_hours}"
        if store.phone:
            part += f"\n📞 Тел.: {store.phone}"
        if store.route_url:
            part += f'\n<a href="{store.route_url}">Проложить Маршрут</a>'
        parts.append(part)
    return "\n\n".join(parts)

def build_pagination(lat: float, lon: float, page: int, total: int):
    builder = InlineKeyboardBuilder()
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    show_prev = page > 1
    show_next = end < total
    lat_str = f"{lat:.5f}"
    lon_str = f"{lon:.5f}"

    if show_prev:
        builder.button(
            text="⬅️ Назад",
            callback_data=f"stores_page:{lat_str}:{lon_str}:{page - 1}",
        )
    if show_next:
        builder.button(
            text="Вперед ➡️",
            callback_data=f"stores_page:{lat_str}:{lon_str}:{page + 1}",
        )
    builder.button(text="🏠 Главное Меню", callback_data="menu")

    if show_prev and show_next:
        builder.adjust(2, 1)
    elif show_prev or show_next:
        builder.adjust(1, 1)
    else:
        builder.adjust(1)
    return builder.as_markup()

@router.message(F.location)
async def show_nearby(message: Message) -> None:
    loc = message.location
    lat = loc.latitude
    lon = loc.longitude
    stores = await provider.list_stores_sorted((lat, lon))
    if not stores:
        await message.answer("😔 Магазины не найдены", reply_markup=menu_markup)
        return

    text = build_page_text(stores, 0, ITEMS_PER_PAGE)
    markup = build_pagination(lat, lon, 1, len(stores))
    await message.answer(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=markup,
        )

@router.callback_query(F.data.startswith("stores_page:"))
async def paginate_stores(call: CallbackQuery) -> None:
    _, lat_str, lon_str, page_str = call.data.split(":")
    page = int(page_str)
    lat = float(lat_str)
    lon = float(lon_str)

    stores = await provider.list_stores_sorted((lat, lon))
    if not stores:
        await call.answer("😔 Нет данных", show_alert=True)
        return

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    text = build_page_text(stores, start, end)
    markup = build_pagination(lat, lon, page, len(stores))
    await call.message.edit_text(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=markup,
    )
    await call.answer()
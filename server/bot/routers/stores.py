from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup

from server.services.data_provider import DataProvider
from ..keyboards import menu_markup

router = Router(name="stores")
provider = DataProvider()

location_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отправить локацию", request_location=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


@router.callback_query(F.data == "stores")
async def request_location(call: CallbackQuery) -> None:
    await call.message.answer(
        "Отправьте свою геолокацию",
        reply_markup=location_keyboard,
    )
    await call.answer()


@router.message(F.location)
async def show_nearby(message: Message) -> None:
    loc = message.location
    stores = await provider.list_stores_sorted((loc.latitude, loc.longitude))
    if not stores:
        await message.answer("Магазины не найдены", reply_markup=menu_markup)
        return
    parts = []
    for store in stores[:5]:
        part = (
            f"<b>{store.name}</b>\n"
            f"Адрес: {store.address}\n"
            f"Расстояние: {store.distance:.1f} км"
        )
        if store.opening_hours:
            part += f"\nВремя работы: {store.opening_hours}"
        if store.phone:
            part += f"\nТел.: {store.phone}"
        if store.route_url:
            part += f"\n[Маршрут]({store.route_url})"
        parts.append(part)
    await message.answer(
        "\n\n".join(parts),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=menu_markup,
    )

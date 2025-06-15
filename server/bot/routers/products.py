from aiogram import Router, F
from aiogram.types import CallbackQuery

from server.services.data_provider import DataProvider
from ..keyboards import menu_markup

router = Router(name="products")
provider = DataProvider()


@router.callback_query(F.data == "products")
async def list_products(call: CallbackQuery) -> None:
    products = await provider.list_products()
    if not products:
        await call.answer("Нет данных", show_alert=True)
        return

    text = "\n".join(f"• {p.name}" for p in products)
    await call.message.answer(text, reply_markup=menu_markup)
    await call.answer()
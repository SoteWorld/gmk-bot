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
    parts = []
    for idx, product in enumerate(products[:10]):
        part = f"<b>{idx + 1}. {product.name}</b>"
        if product.ingredients:
            part += f"\nСостав: {product.ingredients}"
        if product.expiration_date:
            part += f"\nСрок годности: {product.expiration_date}"
        parts.append(part)

    await call.message.answer(
        "\n\n".join(parts), parse_mode="HTML", reply_markup=menu_markup
    )
    await call.answer()


@router.callback_query(F.data.startswith("product:"))
async def paginate_products(call: CallbackQuery) -> None:
    products = await provider.list_products()
    if not products:
        await call.answer("Нет данных", show_alert=True)
        return

    index = int(call.data.split(":")[1])
    if index < 0 or index >= len(products):
        await call.answer()
        return

    await call.message.delete()
    await _send_product(call.message, index, products)
    await call.answer()

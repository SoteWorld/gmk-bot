from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from server.services.data_provider import DataProvider
from ..keyboards import product_nav_markup

router = Router(name="products")
provider = DataProvider()


def _format_product(product, index: int, total: int) -> str:
    text = f"<b>{product.name}</b>"
    if product.ingredients:
        text += f"\nСостав: {product.ingredients}"
    if product.expiration_date:
        text += f"\nСрок годности: {product.expiration_date}"
    text += f"\n\n{index + 1} из {total}"
    return text


async def _send_product(message: Message, index: int, products) -> None:
    product = products[index]
    text = _format_product(product, index, len(products))
    markup = product_nav_markup(index, len(products))
    if product.image:
        await message.answer_photo(product.image, caption=text, parse_mode="HTML", reply_markup=markup)
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=markup)


@router.callback_query(F.data == "products")
async def list_products(call: CallbackQuery) -> None:
    products = await provider.list_products()
    if not products:
        await call.answer("Нет данных", show_alert=True)
        return

    await _send_product(call.message, 0, products)
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

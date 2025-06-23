from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from server.services.data_provider import DataProvider
from ..keyboards import menu_markup

router = Router(name="products")
provider = DataProvider()

# Mapping of internal category codes to user-friendly Russian names
CATEGORY_TRANSLATIONS = {
    "fresh": "Новинки",
    "sausages": "Сосиски и сардельки",
    "smoked_meats": "Копчености",
    "boiled_sausage": "Вареные колбасы",
    "boiled_sausages": "Вареные колбасы",
    "cooked-smoked_semi-smoked": "В/К колбасы, полукопченые колбасы",
    "semi_finished": "Полуфабрикаты",
    "dumplings": "Пельмени",
    "other": "Прочие изделия",
    "raw-smoked_dry-cured": "Сырокопченые, сыровяленые колбасы",
    "raw-smoked_dry-cyred": "Сырокопченые, сыровяленые колбасы",
}

@router.callback_query(F.data == "products")
async def choose_category(call: CallbackQuery) -> None:
    categories = await provider.list_categories()
    if not categories:
        await call.answer("Нет данных", show_alert=True)
        return

    builder = InlineKeyboardBuilder()
    for cat in categories:
        text = CATEGORY_TRANSLATIONS.get(cat, cat)
        builder.button(text=text, callback_data=f"category:{cat}")
    builder.adjust(1)

    await call.message.answer(
        "Выберите категорию:", reply_markup=builder.as_markup()
    )
    await call.answer()


@router.callback_query(F.data.startswith("category:"))
async def list_products(call: CallbackQuery) -> None:
    category = call.data.split(":", 1)[1]
    products = await provider.list_products_by_category(category)
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
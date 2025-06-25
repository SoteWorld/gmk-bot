from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from server.services.data_provider import DataProvider
from server.constants import ITEMS_PER_PAGE

router = Router(name="products")
provider = DataProvider()

# Mapping of internal category codes to user-friendly Russian names
CATEGORY_TRANSLATIONS = {
    "fresh": "🆕 Новинки",
    "sausages": "🌭 Сосиски и сардельки",
    "smoked_meats": "🍖 Копчености",
    "boiled_sausage": "🥪 Вареные колбасы",
    "boiled_sausages": "🥪 Вареные колбасы",
    "cooked-smoked_semi-smoked": "🥓 В/К колбасы, полукопченые колбасы",
    "semi_finished": "🍳 Полуфабрикаты",
    "dumplings": "🥟 Пельмени",
    "other": "🍲 Прочие изделия",
    "raw-smoked_dry-cured": "🍢 Сырокопченые, сыровяленые колбасы",
    "raw-smoked_dry-cyred": "🍢 Сырокопченые, сыровяленые колбасы",
}

@router.callback_query(F.data == "products")
async def choose_category(call: CallbackQuery) -> None:
    categories = await provider.list_categories()
    if not categories:
        await call.answer("😔 Нет данных", show_alert=True)
        return

    builder = InlineKeyboardBuilder()
    for cat in categories:
        text = CATEGORY_TRANSLATIONS.get(cat, cat)
        builder.button(text=text, callback_data=f"category:{cat}")
    builder.adjust(1)

    await call.message.edit_text(
        "📂 Пожалуйста, выберите интересующую вас категорию товаров:",
        reply_markup=builder.as_markup(),
    )
    await call.answer()




@router.callback_query(F.data.startswith("category:"))
async def list_products(call: CallbackQuery) -> None:
    data_parts = call.data.split(":")
    category = data_parts[1]
    page = int(data_parts[2]) if len(data_parts) > 2 else 1

    products = await provider.list_products_by_category(category)
    if not products:
        await call.answer("😔 Нет данных", show_alert=True)
        return

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_products = products[start:end]

    text_parts = []
    for idx, product in enumerate(page_products, start=start + 1):
        part = f"<b>{idx}. {product.name}</b>"
        if product.ingredients:
            part += f"\n🍖 Состав: {product.ingredients}"
        if product.expiration_date:
            part += f"\n⏳ Срок годности: {product.expiration_date}"
        text_parts.append(part)

    builder = InlineKeyboardBuilder()
    show_prev = page > 1
    show_next = end < len(products)
    if show_prev:
        builder.button(text="⬅️ Назад", callback_data=f"category:{category}:{page - 1}")
    if show_next:
        builder.button(text="Вперед ➡️", callback_data=f"category:{category}:{page + 1}")
    builder.button(text="🏠 Главное Меню", callback_data="menu")

    if show_prev and show_next:
        builder.adjust(2, 1)
    elif show_prev or show_next:
        builder.adjust(1, 1)
    else:
        builder.adjust(1)

    await call.message.edit_text(
        "\n\n".join(text_parts), parse_mode="HTML", reply_markup=builder.as_markup()
    )
    await call.answer()

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.keyboard import InlineKeyboardBuilder
 
from config import config
from database.models import get_categories, get_products, get_product, get_category, add_to_cart, upsert_user, get_car
from keyboards.inline import categories_kb, products_kb, product_detail_kb, main_menu_kb, car_categories_kb, car_products_kb
 
router = Router()
 
 
def format_product(p: dict) -> str:
    car_info = f"\n🚗 Для: {p['brand']} {p['model']}" if p.get("brand") else ""
    stock_info = "✅ В наличии" if p["stock"] > 0 else "❌ Нет в наличии"
    return (
        f"🔩 <b>{p['name']}</b>\n"
        f"📋 Артикул: {p.get('article') or '—'}\n"
        f"📁 Категория: {p.get('category_name') or '—'}"
        f"{car_info}\n"
        f"💰 Цена: <b>{p['price']} ₽</b>\n"
        f"📦 {stock_info} (остаток: {p['stock']} шт.)\n\n"
        f"{p.get('description') or ''}"
    )
 
 
@router.callback_query(F.data.startswith("menu:parts:"))
async def cb_parts_categories(callback: CallbackQuery):
    page = int(callback.data.split(":")[2])
    cats, total = await get_categories(page, config.ITEMS_PER_PAGE)
    if not cats:
        text = "🔧 <b>Автозапчасти</b>\n\nКатегории пусты."
        kb = main_menu_kb()
    else:
        text = f"🔧 <b>Автозапчасти</b>\n\nВыберите категорию (всего: {total}):"
        kb = categories_kb(cats, page, total, config.ITEMS_PER_PAGE, "parts")
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
 
 
@router.callback_query(F.data.startswith("cat:parts:"))
async def cb_category_products(callback: CallbackQuery):
    parts = callback.data.split(":")
    cat_id = int(parts[2])
    page = int(parts[3])
    cat = await get_category(cat_id)
    products, total = await get_products(page, config.ITEMS_PER_PAGE, category_id=cat_id)
    cat_name = cat["name"] if cat else "Категория"
    if not products:
        text = f"📁 <b>{cat_name}</b>\n\nТоваров нет."
        await callback.message.edit_text(text, reply_markup=main_menu_kb())
    else:
        text = f"📁 <b>{cat_name}</b> (товаров: {total})\n\nВыберите товар:"
        kb = products_kb(products, page, total, config.ITEMS_PER_PAGE, cat_id)
        await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
 
 
@router.callback_query(F.data.startswith("carparts:"))
async def cb_car_parts_categories(callback: CallbackQuery):
    parts = callback.data.split(":")
    car_id = int(parts[1])
    page = int(parts[2])
    car = await get_car(car_id)
    car_name = f"{car['brand']} {car['model']}" if car else f"авто #{car_id}"
    cats, total = await get_categories(page, config.ITEMS_PER_PAGE)
    if not cats:
        await callback.message.edit_text("Категории не найдены.", reply_markup=main_menu_kb())
    else:
        text = f"🔧 <b>Запчасти для {car_name}</b>\n\nВыберите категорию:"
        kb = car_categories_kb(cats, car_id, page, total, config.ITEMS_PER_PAGE)
        await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
 
 
@router.callback_query(F.data.startswith("carcat:"))
async def cb_car_category_products(callback: CallbackQuery):
    parts = callback.data.split(":")
    car_id = int(parts[1])
    cat_id = int(parts[2])
    page = int(parts[3])
    cat = await get_category(cat_id)
    car = await get_car(car_id)
    products, total = await get_products(page, config.ITEMS_PER_PAGE, category_id=cat_id, car_id=car_id)
    cat_name = cat["name"] if cat else "Категория"
    car_name = f"{car['brand']} {car['model']}" if car else ""
    if not products:
        b = InlineKeyboardBuilder()
        b.button(text="◀️ К категориям", callback_data=f"carparts:{car_id}:1")
        b.button(text="🏠 Главное меню", callback_data="menu:main")
        b.adjust(1)
        text = f"📁 <b>{cat_name}</b> для {car_name}\n\nТоваров для этого автомобиля нет в данной категории."
        await callback.message.edit_text(text, reply_markup=b.as_markup())
    else:
        text = f"📁 <b>{cat_name}</b> для {car_name} (товаров: {total})\n\nВыберите товар:"
        kb = car_products_kb(products, car_id, cat_id, page, total, config.ITEMS_PER_PAGE)
        await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
 
 
@router.callback_query(F.data.startswith("product:view:"))
async def cb_product_view(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[2])
    p = await get_product(product_id)
    if not p:
        await callback.answer("Товар не найден", show_alert=True)
        return
    text = format_product(p)
    kb = product_detail_kb(product_id, p.get("category_id") or 1)
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
 
 
@router.callback_query(F.data.startswith("cart:add:"))
async def cb_add_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[2])
    await upsert_user(
        callback.from_user.id,
        callback.from_user.username or "",
        callback.from_user.full_name or ""
    )
    p = await get_product(product_id)
    if not p:
        await callback.answer("Товар не найден", show_alert=True)
        return
    if p["stock"] <= 0:
        await callback.answer("❌ Товара нет в наличии", show_alert=True)
        return
    await add_to_cart(callback.from_user.id, product_id)
    await callback.answer(f"✅ «{p['name']}» добавлен в корзину!", show_alert=True)
 
 
@router.inline_query(F.query.startswith("product_"))
async def inline_share_product(query: InlineQuery):
    try:
        product_id = int(query.query.split("_")[1])
        p = await get_product(product_id)
        if not p:
            await query.answer([])
            return
        text = (
            f"🔩 <b>{p['name']}</b>\n"
            f"💰 Цена: {p['price']} ₽\n"
            f"📋 Артикул: {p.get('article') or '—'}\n\n"
            f"Смотрите в нашем магазине автозапчастей!"
        )
        result = InlineQueryResultArticle(
            id=str(product_id),
            title=p["name"],
            description=f"{p['price']} ₽ | {p.get('article') or ''}",
            input_message_content=InputTextMessageContent(
                message_text=text,
                parse_mode="HTML"
            )
        )
        await query.answer([result], cache_time=60)
    except Exception:
        await query.answer([])
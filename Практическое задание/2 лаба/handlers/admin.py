from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Filter, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from config import config
from database.models import (
    get_cars, get_car, create_car, update_car, delete_car,
    get_categories, get_category, create_category, update_category, delete_category,
    get_products, get_product, create_product, update_product, delete_product,
    get_all_orders_admin, update_order_status, get_stats
)
from keyboards.inline import (admin_main_kb, admin_list_kb, stats_period_kb,
                               confirm_kb, main_menu_kb)

router = Router()

class IsAdmin(Filter):
    async def __call__(self, event) -> bool:
        user_id = event.from_user.id if hasattr(event, 'from_user') else 0
        return user_id in config.ADMIN_IDS

def cancel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отмена", callback_data="admin:main")
    return builder.as_markup()

class AdminCarForm(StatesGroup):
    brand = State()
    model = State()
    year_from = State()
    year_to = State()
    description = State()
    edit_id = State()

class AdminCatForm(StatesGroup):
    name = State()
    description = State()
    edit_id = State()

class AdminProductForm(StatesGroup):
    name = State()
    description = State()
    price = State()
    stock = State()
    category_id = State()
    car_id = State()
    article = State()
    edit_id = State()

@router.callback_query(IsAdmin(), F.data == "admin:main")
# главная страница админки
async def cb_admin_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔐 <b>Административная панель</b>\n\nВыберите раздел:",
        reply_markup=admin_main_kb()
    )
    await callback.answer()

@router.callback_query(IsAdmin(), F.data == "admin:stats")
# статистика
async def cb_admin_stats(callback: CallbackQuery):
    await callback.message.edit_text(
        "📊 <b>Статистика</b>\n\nВыберите период:",
        reply_markup=stats_period_kb()
    )
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("admin:stats:"))
async def cb_admin_stats_period(callback: CallbackQuery):
    days = int(callback.data.split(":")[2])
    period_name = {1: "сегодня", 7: "7 дней", 30: "30 дней"}.get(days, f"{days} дней")
    stats = await get_stats(days)
    text = (
        f"📊 <b>Статистика за {period_name}</b>\n\n"
        f"👤 Посетителей: <b>{stats['visitors']}</b>\n"
        f"📦 Продано товаров: <b>{stats['sold']}</b>\n"
        f"💰 Выручка: <b>{stats['revenue']:.2f} ₽</b>\n"
    )
    await callback.message.edit_text(text, reply_markup=stats_period_kb())
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("admin:cars:"), ~F.data.contains("add"), ~F.data.contains("edit"), ~F.data.contains("del"))
async def cb_admin_cars(callback: CallbackQuery):
    parts = callback.data.split(":")
    page = int(parts[2])
    cars, total = await get_cars(page, config.ITEMS_PER_PAGE)
    await callback.message.edit_text(
        f"🚗 <b>Управление автомобилями</b> (всего: {total})",
        reply_markup=admin_list_kb(cars, "cars", page, total, config.ITEMS_PER_PAGE)
    )
    await callback.answer()

@router.callback_query(IsAdmin(), F.data == "admin:cars:add")
async def cb_admin_car_add(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminCarForm.brand)
    await state.update_data(edit_id=None)
    await callback.message.edit_text("➕ <b>Новый автомобиль</b>\n\nВведите марку:\n/cancel — отмена", reply_markup=cancel_kb())
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("admin:cars:edit:"))
async def cb_admin_car_edit(callback: CallbackQuery, state: FSMContext):
    car_id = int(callback.data.split(":")[3])
    car = await get_car(car_id)
    await state.set_state(AdminCarForm.brand)
    await state.update_data(edit_id=car_id)
    await callback.message.edit_text(
        f"✏️ Редактирование: {car['brand']} {car['model']}\n\nВведите марку:\n/cancel — отмена",
        reply_markup=cancel_kb()
    )
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("admin:cars:del:"))
async def cb_admin_car_del(callback: CallbackQuery):
    car_id = int(callback.data.split(":")[3])
    await callback.message.edit_text(
        "⚠️ Удалить автомобиль?",
        reply_markup=confirm_kb("car", car_id)
    )
    await callback.answer()

@router.message(IsAdmin(), AdminCarForm.brand)
async def admin_car_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text.strip())
    await state.set_state(AdminCarForm.model)
    await message.answer("Модель:")

@router.message(IsAdmin(), AdminCarForm.model)
async def admin_car_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text.strip())
    await state.set_state(AdminCarForm.year_from)
    await message.answer("Год выпуска (от):")

@router.message(IsAdmin(), AdminCarForm.year_from)
async def admin_car_year_from(message: Message, state: FSMContext):
    await state.update_data(year_from=int(message.text))
    await state.set_state(AdminCarForm.year_to)
    await message.answer("Год выпуска (до), 0 = сейчас:")

@router.message(IsAdmin(), AdminCarForm.year_to)
async def admin_car_year_to(message: Message, state: FSMContext):
    val = int(message.text)
    await state.update_data(year_to=val if val > 0 else None)
    await state.set_state(AdminCarForm.description)
    await message.answer("Описание (или '-'):")

@router.message(IsAdmin(), AdminCarForm.description)
async def admin_car_desc(message: Message, state: FSMContext):
    data = await state.get_data()
    desc = message.text.strip() if message.text.strip() != "-" else ""
    if data.get("edit_id"):
        await update_car(data["edit_id"], data["brand"], data["model"], data["year_from"], data.get("year_to"), desc)
        await message.answer("✅ Обновлено!", reply_markup=admin_main_kb())
    else:
        await create_car(data["brand"], data["model"], data["year_from"], data.get("year_to"), desc)
        await message.answer("✅ Добавлено!", reply_markup=admin_main_kb())
    await state.clear()

@router.callback_query(IsAdmin(), F.data.startswith("admin:cats:"), ~F.data.contains("add"), ~F.data.contains("edit"), ~F.data.contains("del"))
async def cb_admin_cats(callback: CallbackQuery):
    parts = callback.data.split(":")
    page = int(parts[2])
    cats, total = await get_categories(page, config.ITEMS_PER_PAGE)
    await callback.message.edit_text(
        f"📁 <b>Управление категориями</b> (всего: {total})",
        reply_markup=admin_list_kb(cats, "cats", page, total, config.ITEMS_PER_PAGE)
    )
    await callback.answer()

@router.callback_query(IsAdmin(), F.data == "admin:cats:add")
async def cb_admin_cat_add(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminCatForm.name)
    await state.update_data(edit_id=None)
    await callback.message.edit_text("➕ <b>Новая категория</b>\n\nВведите название:\n/cancel — отмена", reply_markup=cancel_kb())
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("admin:cats:edit:"))
async def cb_admin_cat_edit(callback: CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split(":")[3])
    await state.set_state(AdminCatForm.name)
    await state.update_data(edit_id=cat_id)
    await callback.message.edit_text("✏️ Редактирование категории\n\nВведите название:\n/cancel — отмена", reply_markup=cancel_kb())
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("admin:cats:del:"))
async def cb_admin_cat_del(callback: CallbackQuery):
    cat_id = int(callback.data.split(":")[3])
    await callback.message.edit_text("⚠️ Удалить категорию?", reply_markup=confirm_kb("cat", cat_id))
    await callback.answer()

@router.message(IsAdmin(), AdminCatForm.name)
async def admin_cat_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AdminCatForm.description)
    await message.answer("Описание (или '-'):")

@router.message(IsAdmin(), AdminCatForm.description)
async def admin_cat_desc(message: Message, state: FSMContext):
    data = await state.get_data()
    desc = message.text.strip() if message.text.strip() != "-" else ""
    if data.get("edit_id"):
        await update_category(data["edit_id"], data["name"], desc)
        await message.answer("✅ Обновлено!", reply_markup=admin_main_kb())
    else:
        await create_category(data["name"], desc)
        await message.answer("✅ Добавлено!", reply_markup=admin_main_kb())
    await state.clear()

@router.callback_query(IsAdmin(), F.data.startswith("admin:products:"), ~F.data.contains("add"), ~F.data.contains("edit"), ~F.data.contains("del"))
async def cb_admin_products(callback: CallbackQuery):
    parts = callback.data.split(":")
    page = int(parts[2])
    products, total = await get_products(page, config.ITEMS_PER_PAGE)
    await callback.message.edit_text(
        f"🔩 <b>Управление товарами</b> (всего: {total})",
        reply_markup=admin_list_kb(products, "products", page, total, config.ITEMS_PER_PAGE)
    )
    await callback.answer()

@router.callback_query(IsAdmin(), F.data == "admin:products:add")
async def cb_admin_product_add(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminProductForm.name)
    await state.update_data(edit_id=None)
    await callback.message.edit_text("➕ <b>Новый товар</b>\n\nВведите название:\n/cancel — отмена", reply_markup=cancel_kb())
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("admin:products:edit:"))
async def cb_admin_product_edit(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[3])
    await state.set_state(AdminProductForm.name)
    await state.update_data(edit_id=product_id)
    await callback.message.edit_text("✏️ Редактирование товара\n\nВведите название:\n/cancel — отмена", reply_markup=cancel_kb())
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("admin:products:del:"))
async def cb_admin_product_del(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[3])
    await callback.message.edit_text("⚠️ Удалить товар?", reply_markup=confirm_kb("product", product_id))
    await callback.answer()

@router.message(IsAdmin(), AdminProductForm.name)
async def admin_product_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text.strip())
    await state.set_state(AdminProductForm.description)
    await msg.answer("Описание:\n/cancel — отмена")

@router.message(IsAdmin(), AdminProductForm.description)
async def admin_product_desc(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text.strip())
    await state.set_state(AdminProductForm.price)
    await msg.answer("Цена (₽):\n/cancel — отмена")

@router.message(IsAdmin(), AdminProductForm.price)
async def admin_product_price(msg: Message, state: FSMContext):
    try:
        price = float(msg.text.replace(",", "."))
        await state.update_data(price=price)
        await state.set_state(AdminProductForm.stock)
        await msg.answer("Остаток (шт.):\n/cancel — отмена")
    except ValueError:
        await msg.answer("Введите число:")

@router.message(IsAdmin(), AdminProductForm.stock)
async def admin_product_stock(msg: Message, state: FSMContext):
    await state.update_data(stock=int(msg.text))
    await state.set_state(AdminProductForm.category_id)
    await msg.answer("ID категории (или 0):\n/cancel — отмена")

@router.message(IsAdmin(), AdminProductForm.category_id)
async def admin_product_cat(msg: Message, state: FSMContext):
    val = int(msg.text)
    await state.update_data(category_id=val if val > 0 else None)
    await state.set_state(AdminProductForm.car_id)
    await msg.answer("ID автомобиля (или 0):\n/cancel — отмена")

@router.message(IsAdmin(), AdminProductForm.car_id)
async def admin_product_car(msg: Message, state: FSMContext):
    val = int(msg.text)
    await state.update_data(car_id=val if val > 0 else None)
    await state.set_state(AdminProductForm.article)
    await msg.answer("Артикул (или '-'):\n/cancel — отмена")

@router.message(IsAdmin(), AdminProductForm.article)
async def admin_product_article(msg: Message, state: FSMContext):
    data = await state.get_data()
    article = msg.text.strip() if msg.text.strip() != "-" else ""
    if data.get("edit_id"):
        await update_product(
            data["edit_id"], data["name"], data["description"], data["price"],
            data["stock"], data.get("category_id"), data.get("car_id"), None, article
        )
        await msg.answer("✅ Товар обновлён!", reply_markup=admin_main_kb())
    else:
        await create_product(
            data["name"], data["description"], data["price"],
            data["stock"], data.get("category_id"), data.get("car_id"), None, article
        )
        await msg.answer("✅ Товар добавлен!", reply_markup=admin_main_kb())
    await state.clear()

@router.callback_query(IsAdmin(), F.data.startswith("admin:orders:"))
async def cb_admin_orders(callback: CallbackQuery):
    page = int(callback.data.split(":")[2])
    orders, total = await get_all_orders_admin(page, config.ITEMS_PER_PAGE)
    if not orders:
        text = "📦 <b>Заказы</b>\n\nЗаказов нет."
        await callback.message.edit_text(text, reply_markup=admin_main_kb())
    else:
        from keyboards.inline import orders_kb
        await callback.message.edit_text(
            f"📦 <b>Все заказы</b> (всего: {total})",
            reply_markup=orders_kb(orders, page, total, config.ITEMS_PER_PAGE, is_admin=True)
        )
    await callback.answer()

@router.callback_query(IsAdmin(), F.data.startswith("confirm:"))
async def cb_confirm_delete(callback: CallbackQuery):
    parts = callback.data.split(":")
    entity = parts[1]
    entity_id = int(parts[2])
    if entity == "car":
        await delete_car(entity_id)
        msg = "🚗 Автомобиль удалён"
    elif entity == "cat":
        await delete_category(entity_id)
        msg = "📁 Категория удалена"
    elif entity == "product":
        await delete_product(entity_id)
        msg = "🔩 Товар удалён"
    else:
        msg = "Удалено"
    await callback.answer(msg, show_alert=True)
    await callback.message.edit_text("✅ " + msg, reply_markup=admin_main_kb())

from aiogram.filters import Command

@router.message(IsAdmin(), Command("cancel"))
async def admin_cancel(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is not None:
        await state.clear()
    await message.answer("🔐 <b>Административная панель</b>", reply_markup=admin_main_kb())

@router.message(IsAdmin(), Command("admin"))
async def cmd_admin(message: Message):
    await message.answer("🔐 <b>Административная панель</b>", reply_markup=admin_main_kb())

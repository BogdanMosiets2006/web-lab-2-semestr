from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import math

# клавиатура главного меню
def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🚗 Автомобили", callback_data="menu:cars:1")
    builder.button(text="🔧 Автозапчасти", callback_data="menu:parts:1")
    builder.button(text="🛒 Корзина", callback_data="menu:cart")
    builder.button(text="📦 Мои заказы", callback_data="menu:orders:1")
    builder.button(text="ℹ️ О приложении", callback_data="menu:about")
    builder.button(text="❓ Помощь", callback_data="menu:help")
    builder.adjust(2, 2, 2)
    return builder.as_markup()

# универсальная пагинация
def pagination_kb(current_page: int, total: int, per_page: int, prefix: str, extra_params: str = "") -> InlineKeyboardMarkup:
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    builder = InlineKeyboardBuilder()
    nav_buttons = []
    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton(
            text="◀️ Назад",
            callback_data=f"{prefix}:{current_page - 1}{extra_params}"
        ))
    nav_buttons.append(InlineKeyboardButton(
        text=f"{current_page}/{total_pages}",
        callback_data="noop"
    ))
    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton(
            text="Вперёд ▶️",
            callback_data=f"{prefix}:{current_page + 1}{extra_params}"
        ))
    builder.row(*nav_buttons)
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"))
    return builder.as_markup()

def cars_list_kb(cars: list, page: int, total: int, per_page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for car in cars:
        years = f"{car['year_from']}-{car['year_to'] or '...'}"
        builder.button(
            text=f"🚗 {car['brand']} {car['model']} ({years})",
            callback_data=f"car:view:{car['id']}"
        )
    builder.adjust(1)
    # Pagination
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"menu:cars:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"menu:cars:{page+1}"))
    builder.row(*nav)
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"))
    return builder.as_markup()

def car_detail_kb(car_id: int, page: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔧 Запчасти для этого авто", callback_data=f"carparts:{car_id}:1")
    builder.button(text="◀️ К списку", callback_data=f"menu:cars:{page}")
    builder.button(text="🏠 Главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()

def categories_kb(categories: list, page: int, total: int, per_page: int, source: str = "parts") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=f"📁 {cat['name']}", callback_data=f"cat:{source}:{cat['id']}:1")
    builder.adjust(1)
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"menu:{source}:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"menu:{source}:{page+1}"))
    builder.row(*nav)
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"))
    return builder.as_markup()

def products_kb(products: list, page: int, total: int, per_page: int, cat_id: int, car_id: int = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in products:
        builder.button(
            text=f"🔩 {p['name']} — {p['price']} ₽",
            callback_data=f"product:view:{p['id']}"
        )
    builder.adjust(1)
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    extra = f":{car_id}" if car_id else ":0"
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"cat:parts:{cat_id}:{page-1}{extra}"))
    nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"cat:parts:{cat_id}:{page+1}{extra}"))
    builder.row(*nav)
    builder.row(InlineKeyboardButton(text="◀️ К категориям", callback_data="menu:parts:1"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"))
    return builder.as_markup()

def product_detail_kb(product_id: int, cat_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🛒 В корзину", callback_data=f"cart:add:{product_id}")
    builder.button(text="📤 Поделиться", switch_inline_query=f"product_{product_id}")
    builder.button(text="◀️ К товарам", callback_data=f"cat:parts:{cat_id}:1")
    builder.button(text="🏠 Главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()

# клавиатура корзины
def cart_kb(cart_items: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in cart_items:
        builder.button(
            text=f"➖ {item['name']}",
            callback_data=f"cart:remove:{item['product_id']}"
        )
    builder.button(text="✅ Оформить заказ", callback_data="cart:checkout")
    builder.button(text="🗑 Очистить корзину", callback_data="cart:clear")
    builder.button(text="🏠 Главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()

def orders_kb(orders: list, page: int, total: int, per_page: int, is_admin: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    status_emoji = {
        "pending": "⏳", "paid": "💰", "processing": "⚙️",
        "shipped": "🚚", "delivered": "✅", "cancelled": "❌"
    }
    for o in orders:
        emoji = status_emoji.get(o["status"], "📦")
        builder.button(
            text=f"{emoji} Заказ #{o['id']} — {o['total_amount']} ₽",
            callback_data=f"order:detail:{o['id']}"
        )
    builder.adjust(1)
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"menu:orders:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"menu:orders:{page+1}"))
    builder.row(*nav)
    if is_admin:
        builder.row(InlineKeyboardButton(text="◀️ Админ-панель", callback_data="admin:main"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"))
    return builder.as_markup()

def order_detail_kb(order_id: int, status: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if status == "pending":
        builder.button(text="💳 Оплатить", callback_data=f"order:pay:{order_id}")
        builder.button(text="❌ Отменить", callback_data=f"order:cancel:{order_id}")
    builder.button(text="◀️ К заказам", callback_data="menu:orders:1")
    builder.button(text="🏠 Главное меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()

def admin_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🚗 Машины", callback_data="admin:cars:1")
    builder.button(text="📁 Категории", callback_data="admin:cats:1")
    builder.button(text="🔩 Товары", callback_data="admin:products:1")
    builder.button(text="📦 Заказы", callback_data="admin:orders:1")
    builder.button(text="📊 Статистика", callback_data="admin:stats")
    builder.button(text="🏠 Главное меню", callback_data="menu:main")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()

def admin_list_kb(items: list, entity: str, page: int, total: int, per_page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        label = item.get("name") or f"{item.get('brand')} {item.get('model')}"
        builder.button(text=f"✏️ {label}", callback_data=f"admin:{entity}:edit:{item['id']}")
        builder.button(text="🗑", callback_data=f"admin:{entity}:del:{item['id']}")
    builder.adjust(2)
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"admin:{entity}:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"admin:{entity}:{page+1}"))
    builder.row(*nav)
    builder.row(InlineKeyboardButton(text="➕ Добавить", callback_data=f"admin:{entity}:add"))
    builder.row(InlineKeyboardButton(text="◀️ Админ-панель", callback_data="admin:main"))
    return builder.as_markup()

def stats_period_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="За сегодня", callback_data="admin:stats:1")
    builder.button(text="За 7 дней", callback_data="admin:stats:7")
    builder.button(text="За 30 дней", callback_data="admin:stats:30")
    builder.button(text="◀️ Админ-панель", callback_data="admin:main")
    builder.adjust(3, 1)
    return builder.as_markup()

def confirm_kb(action: str, entity_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, удалить", callback_data=f"confirm:{action}:{entity_id}")
    builder.button(text="❌ Отмена", callback_data="admin:main")
    builder.adjust(2)
    return builder.as_markup()

def car_categories_kb(categories: list, car_id: int, page: int, total: int, per_page: int) -> InlineKeyboardMarkup:
    import math
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=f"📁 {cat['name']}", callback_data=f"carcat:{car_id}:{cat['id']}:1")
    builder.adjust(1)
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"carparts:{car_id}:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"carparts:{car_id}:{page+1}"))
    builder.row(*nav)
    builder.row(InlineKeyboardButton(text="◀️ К авто", callback_data=f"car:view:{car_id}"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"))
    return builder.as_markup()

def car_products_kb(products: list, car_id: int, cat_id: int, page: int, total: int, per_page: int) -> InlineKeyboardMarkup:
    import math
    builder = InlineKeyboardBuilder()
    for p in products:
        builder.button(text=f"🔩 {p['name']} — {p['price']} ₽", callback_data=f"product:view:{p['id']}")
    builder.adjust(1)
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"carcat:{car_id}:{cat_id}:{page-1}"))
    nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"carcat:{car_id}:{cat_id}:{page+1}"))
    builder.row(*nav)
    builder.row(InlineKeyboardButton(text="◀️ К категориям", callback_data=f"carparts:{car_id}:1"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"))
    return builder.as_markup()

from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import config
from database.models import get_orders, get_order_detail, update_order_status
from keyboards.inline import orders_kb, order_detail_kb, main_menu_kb

router = Router()

STATUS_RU = {
    "pending": "⏳ Ожидает оплаты",
    "paid": "💰 Оплачен",
    "processing": "⚙️ В обработке",
    "shipped": "🚚 Отправлен",
    "delivered": "✅ Доставлен",
    "cancelled": "❌ Отменён",
}

@router.callback_query(F.data.startswith("menu:orders:"))
async def cb_orders_list(callback: CallbackQuery):
    page = int(callback.data.split(":")[2])
    orders, total = await get_orders(callback.from_user.id, page, config.ITEMS_PER_PAGE)
    if not orders:
        await callback.message.edit_text(
            "📦 <b>Мои заказы</b>\n\nУ вас пока нет заказов.",
            reply_markup=main_menu_kb()
        )
    else:
        await callback.message.edit_text(
            f"📦 <b>Мои заказы</b> (всего: {total})",
            reply_markup=orders_kb(orders, page, total, config.ITEMS_PER_PAGE)
        )
    await callback.answer()

@router.callback_query(F.data.startswith("order:detail:"))
async def cb_order_detail(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[2])
    order, items = await get_order_detail(order_id)
    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return
    lines = [
        f"📦 <b>Заказ #{order_id}</b>\n",
        f"📅 Дата: {order['created_at'].strftime('%d.%m.%Y %H:%M')}",
        f"🔖 Статус: {STATUS_RU.get(order['status'], order['status'])}",
        f"📍 Адрес: {order.get('delivery_address') or '—'}",
        "\n<b>Состав заказа:</b>",
    ]
    for item in items:
        lines.append(f"• {item['name']} × {item['quantity']} = {float(item['price']) * item['quantity']:.2f} ₽")
    lines.append(f"\n💰 <b>Итого: {float(order['total_amount']):.2f} ₽</b>")

    await callback.message.edit_text(
        "\n".join(lines),
        reply_markup=order_detail_kb(order_id, order["status"])
    )
    await callback.answer()

@router.callback_query(F.data.startswith("order:cancel:"))
async def cb_order_cancel(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[2])
    await update_order_status(order_id, "cancelled")
    await callback.answer("❌ Заказ отменён", show_alert=True)
    await callback.message.edit_text(
        f"❌ Заказ #{order_id} отменён.",
        reply_markup=main_menu_kb()
    )

@router.callback_query(F.data.startswith("order:pay:"))
async def cb_order_pay(callback: CallbackQuery):
    # Payment is initiated fresh from cart; here we just notify
    await callback.answer(
        "Для оплаты оформите новый заказ через корзину.",
        show_alert=True
    )

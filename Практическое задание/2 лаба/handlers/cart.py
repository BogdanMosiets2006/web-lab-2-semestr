from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import config
from database.models import (get_cart, update_cart_item, clear_cart,
                              create_order, create_order_items, update_order_status, get_order_detail)
from keyboards.inline import cart_kb, main_menu_kb
from utils.email import send_order_email

router = Router()

class CheckoutForm(StatesGroup):
    address = State()
    order_id = State()

def format_cart(items: list) -> str:
    if not items:
        return "🛒 <b>Ваша корзина пуста</b>"
    lines = ["🛒 <b>Ваша корзина:</b>\n"]
    total = 0
    for item in items:
        lines.append(f"• {item['name']} × {item['quantity']} = {item['subtotal']} ₽")
        total += float(item["subtotal"])
    lines.append(f"\n💰 <b>Итого: {total:.2f} ₽</b>")
    return "\n".join(lines)

@router.callback_query(F.data == "menu:cart")
# показываем корзину пользователя
async def cb_cart(callback: CallbackQuery):
    items = await get_cart(callback.from_user.id)
    text = format_cart(items)
    kb = cart_kb(items) if items else main_menu_kb()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("cart:remove:"))
async def cb_cart_remove(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[2])
    await update_cart_item(callback.from_user.id, product_id, 0)
    items = await get_cart(callback.from_user.id)
    text = format_cart(items)
    kb = cart_kb(items) if items else main_menu_kb()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer("Товар удалён из корзины")

@router.callback_query(F.data == "cart:clear")
async def cb_cart_clear(callback: CallbackQuery):
    await clear_cart(callback.from_user.id)
    await callback.message.edit_text("🛒 Корзина очищена.", reply_markup=main_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "cart:checkout")
# начинаем оформление заказа
async def cb_checkout_start(callback: CallbackQuery, state: FSMContext):
    items = await get_cart(callback.from_user.id)
    if not items:
        await callback.answer("Корзина пуста!", show_alert=True)
        return
    await state.set_state(CheckoutForm.address)
    await callback.message.edit_text(
        "📦 <b>Оформление заказа</b>\n\n"
        "Введите адрес доставки:\n"
        "<i>(или отправьте /cancel для отмены)</i>"
    )
    await callback.answer()

@router.message(CheckoutForm.address)
async def fsm_checkout_address(message: Message, state: FSMContext):
    address = message.text.strip()
    items = await get_cart(message.from_user.id)
    if not items:
        await message.answer("Корзина пуста!", reply_markup=main_menu_kb())
        await state.clear()
        return

    total = sum(float(i["subtotal"]) for i in items)
    order_id = await create_order(message.from_user.id, total, address)
    order_items = [{"product_id": i["product_id"], "quantity": i["quantity"], "price": i["price"]} for i in items]
    await create_order_items(order_id, order_items)
    await clear_cart(message.from_user.id)

    await state.update_data(order_id=order_id)
    await state.set_state(CheckoutForm.order_id)

    # Send invoice via Telegram Payments
    prices = [LabeledPrice(label=i["name"], amount=int(float(i["price"]) * 100 * i["quantity"])) for i in items]
    try:
        await message.answer_invoice(
            title=f"Заказ #{order_id}",
            description=f"Доставка: {address}\nТоваров: {len(items)} позиций",
            payload=f"order_{order_id}",
            provider_token=config.PAYMENT_PROVIDER_TOKEN,
            currency="RUB",
            prices=prices,
            start_parameter=f"order_{order_id}",
            protect_content=True,
        )
    except Exception as e:
        # Fallback if payment provider not configured
        await update_order_status(order_id, "pending")
        await message.answer(
            f"✅ <b>Заказ #{order_id} создан!</b>\n\n"
            f"💰 Сумма: {total:.2f} ₽\n"
            f"📍 Адрес: {address}\n\n"
            "⚠️ Платёжный провайдер не настроен. Менеджер свяжется с вами для оплаты.",
            reply_markup=main_menu_kb()
        )
        await send_order_email(order_id, message.from_user, items, total, address)
        await state.clear()

@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
# обработка успешной оплаты
async def successful_payment(message: Message, state: FSMContext):
    payment = message.successful_payment
    payload = payment.invoice_payload  # "order_{id}"
    order_id = int(payload.split("_")[1])
    payment_id = payment.telegram_payment_charge_id

    await update_order_status(order_id, "paid", payment_id)
    order, items = await get_order_detail(order_id)

    total = float(order["total_amount"])
    await send_order_email(order_id, message.from_user, items, total, order.get("delivery_address", ""))

    await message.answer(
        f"✅ <b>Оплата прошла успешно!</b>\n\n"
        f"🧾 Заказ #{order_id}\n"
        f"💰 Сумма: {total:.2f} ₽\n"
        f"🆔 Транзакция: {payment_id}\n\n"
        "Спасибо за покупку! Мы приступим к обработке вашего заказа.",
        reply_markup=main_menu_kb()
    )
    await state.clear()

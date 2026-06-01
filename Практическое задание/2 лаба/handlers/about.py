from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

ABOUT_TEXT = (
    "ℹ️ <b>О приложении</b>\n\n"
    "🔩 <b>АвтоЗапчасти</b> — интернет-магазин автомобильных запчастей.\n\n"
    "📋 <b>Возможности:</b>\n"
    "• Каталог автомобилей и запчастей\n"
    "• Удобная корзина и оформление заказа\n"
    "• Оплата прямо в Telegram\n"
    "• История заказов\n"
    "• Поиск запчастей по марке авто\n\n"
    "📞 <b>Контакты:</b>\n"
    "Телефон: +7 (800) 555-35-35\n"
    "Email: shop@autoparts.ru"
)

HELP_TEXT = (
    "❓ <b>Помощь</b>\n\n"
    "<b>Как найти запчасть?</b>\n"
    "1. Откройте раздел «Автозапчасти»\n"
    "2. Выберите категорию\n"
    "3. Найдите нужный товар\n\n"
    "<b>Как оформить заказ?</b>\n"
    "1. Добавьте товары в корзину\n"
    "2. Откройте корзину и нажмите «Оформить заказ»\n"
    "3. Укажите адрес доставки\n"
    "4. Оплатите заказ\n\n"
    "<b>Статусы заказа:</b>\n"
    "⏳ Ожидает оплаты → 💰 Оплачен → ⚙️ Обрабатывается → 🚚 Отправлен → ✅ Доставлен\n\n"
    "<b>Поделиться товаром:</b>\n"
    "На странице товара нажмите «📤 Поделиться»\n\n"
    "Если у вас возникли вопросы, напишите нам: @autoparts_support"
)

def back_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Главное меню", callback_data="menu:main")
    return builder.as_markup()

@router.callback_query(F.data == "menu:about")
async def cb_about(callback: CallbackQuery):
    await callback.message.edit_text(ABOUT_TEXT, reply_markup=back_kb())
    await callback.answer()

@router.callback_query(F.data == "menu:help")
async def cb_help(callback: CallbackQuery):
    await callback.message.edit_text(HELP_TEXT, reply_markup=back_kb())
    await callback.answer()

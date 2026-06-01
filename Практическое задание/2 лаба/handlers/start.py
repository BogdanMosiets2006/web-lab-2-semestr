from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from database.models import upsert_user
from keyboards.inline import main_menu_kb

router = Router()

WELCOME_TEXT = (
    "👋 <b>Добро пожаловать в магазин автозапчастей!</b>\n\n"
    "Здесь вы найдёте широкий ассортимент запчастей для вашего автомобиля.\n"
    "Выберите раздел в меню ниже:"
)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await upsert_user(
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.full_name or ""
    )
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb())

@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer()

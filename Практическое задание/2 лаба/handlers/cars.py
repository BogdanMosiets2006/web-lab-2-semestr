from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from config import config
from database.models import get_cars, get_car, create_car, update_car, delete_car
from keyboards.inline import cars_list_kb, car_detail_kb, main_menu_kb

router = Router()

class CarForm(StatesGroup):
    brand = State()
    model = State()
    year_from = State()
    year_to = State()
    description = State()
    editing_id = State()

def format_car(car: dict) -> str:
    years = f"{car['year_from']}–{car['year_to'] or 'н.в.'}"
    return (
        f"🚗 <b>{car['brand']} {car['model']}</b>\n"
        f"📅 Годы выпуска: {years}\n"
        f"📝 {car.get('description') or 'Описание отсутствует'}"
    )

@router.callback_query(F.data.startswith("menu:cars:"))
async def cb_cars_list(callback: CallbackQuery):
    page = int(callback.data.split(":")[2])
    cars, total = await get_cars(page, config.ITEMS_PER_PAGE)
    if not cars:
        text = "🚗 <b>Автомобили</b>\n\nСписок автомобилей пуст."
        kb = main_menu_kb()
    else:
        text = f"🚗 <b>Автомобили</b> (всего: {total})\n\nВыберите автомобиль:"
        kb = cars_list_kb(cars, page, total, config.ITEMS_PER_PAGE)
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("car:view:"))
async def cb_car_view(callback: CallbackQuery):
    car_id = int(callback.data.split(":")[2])
    car = await get_car(car_id)
    if not car:
        await callback.answer("Автомобиль не найден", show_alert=True)
        return
    await callback.message.edit_text(format_car(car), reply_markup=car_detail_kb(car_id))
    await callback.answer()

@router.callback_query(F.data.startswith("car:delete:"))
async def cb_car_delete(callback: CallbackQuery):
    car_id = int(callback.data.split(":")[2])
    await delete_car(car_id)
    await callback.answer("✅ Автомобиль удалён", show_alert=True)
    cars, total = await get_cars(1, config.ITEMS_PER_PAGE)
    text = f"🚗 <b>Автомобили</b> (всего: {total})"
    await callback.message.edit_text(text, reply_markup=cars_list_kb(cars, 1, total, config.ITEMS_PER_PAGE))

@router.callback_query(F.data.startswith("car:edit:"))
async def cb_car_edit(callback: CallbackQuery, state: FSMContext):
    car_id = int(callback.data.split(":")[2])
    car = await get_car(car_id)
    if not car:
        await callback.answer("Не найдено", show_alert=True)
        return
    await state.set_state(CarForm.brand)
    await state.update_data(editing_id=car_id)
    await callback.message.edit_text(
        f"✏️ <b>Редактирование:</b> {car['brand']} {car['model']}\n\n"
        "Введите новую марку автомобиля (или отправьте /cancel):"
    )
    await callback.answer()

@router.message(CarForm.brand, ~F.text.startswith("/"))
async def fsm_car_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text.strip())
    await state.set_state(CarForm.model)
    await message.answer("Введите модель:")

@router.message(CarForm.model, ~F.text.startswith("/"))
async def fsm_car_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text.strip())
    await state.set_state(CarForm.year_from)
    await message.answer("Введите год выпуска (от):")

@router.message(CarForm.year_from, ~F.text.startswith("/"))
async def fsm_car_year_from(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число, например 2010:")
        return
    await state.update_data(year_from=int(message.text))
    await state.set_state(CarForm.year_to)
    await message.answer("Введите год выпуска (до), или 0 если выпускается сейчас:")

@router.message(CarForm.year_to, ~F.text.startswith("/"))
async def fsm_car_year_to(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число:")
        return
    val = int(message.text)
    await state.update_data(year_to=val if val > 0 else None)
    await state.set_state(CarForm.description)
    await message.answer("Введите описание (или '-' чтобы пропустить):")

@router.message(CarForm.description, ~F.text.startswith("/"))
async def fsm_car_description(message: Message, state: FSMContext):
    data = await state.get_data()
    desc = message.text.strip() if message.text.strip() != "-" else ""
    editing_id = data.get("editing_id")

    if editing_id:
        await update_car(editing_id, data["brand"], data["model"], data["year_from"], data.get("year_to"), desc)
        await message.answer("✅ Автомобиль обновлён!", reply_markup=main_menu_kb())
    else:
        car_id = await create_car(data["brand"], data["model"], data["year_from"], data.get("year_to"), desc)
        await message.answer(f"✅ Автомобиль добавлен (ID: {car_id})!", reply_markup=main_menu_kb())

    await state.clear()

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    current = await state.get_state()
    if current is not None:
        await state.clear()
        await message.answer("❌ Действие отменено.", reply_markup=main_menu_kb())
    else:
        await message.answer("Нечего отменять.", reply_markup=main_menu_kb())

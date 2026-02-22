from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_clients, get_orders, delete_order

async def add_order_cmd(message: types.Message):
    clients = get_clients()
    if not clients:
        await message.answer("⚠️ Avval klient qo‘shing: /add_client")
        return

    text = "Mavjud klientlar:\n"
    for c in clients:
        text += f"{c[0]}. {c[1]}\n"
    text += (
        "\nBuyurtma qo‘shish uchun: `client_id, mahsulot, miqdor`\n"
        "Misol: `1, T-shirt, 5`"
    )
    await message.answer(text)

async def show_orders_for_delete(message: types.Message):
    orders = get_orders()
    if not orders:
        await message.answer("📭 Buyurtma mavjud emas.")
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    for o in orders:
        text = f"❌ {o[1]} - {o[2]} ({o[3]} dona) [{o[4]}]"
        keyboard.add(InlineKeyboardButton(
            text=text[:50] + "..." if len(text) > 50 else text,  # uzun matnni qisqartirish
            callback_data=f"del_order:{o[0]}"
        ))
    await message.answer("O'chirmoqchi bo'lgan buyurtmani tanlang:", reply_markup=keyboard)

async def delete_order_callback(callback: types.CallbackQuery):
    order_id = int(callback.data.split(":")[1])
    success, error = delete_order(order_id)
    if success:
        await callback.answer("✅ Buyurtma o'chirildi")
        await callback.message.edit_text(f"Buyurtma (ID: {order_id}) o'chirildi.")
    else:
        await callback.answer("❌ Xatolik: " + (error or "Noma'lum xato"), show_alert=True)
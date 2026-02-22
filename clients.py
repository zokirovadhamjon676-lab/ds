from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_clients, delete_client

async def add_client_cmd(message: types.Message):
    await message.answer(
        "Ism va telefon raqamini vergul bilan ajratib yozing.\n"
        "Misol: `Adham, 998901234567`"
    )

async def list_clients_handler(message: types.Message):
    clients = get_clients()
    if clients:
        text = "📋 Klientlar ro'yxati:\n\n"
        for c in clients:
            text += f"{c[0]}. {c[1]}\n"
        await message.answer(text)
    else:
        await message.answer("⚠️ Hozircha klient yo‘q.")

async def show_clients_for_delete(message: types.Message):
    clients = get_clients()
    if not clients:
        await message.answer("⚠️ Hozircha klient yo‘q.")
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    for c in clients:
        keyboard.add(InlineKeyboardButton(
            text=f"❌ {c[1]} (ID: {c[0]})",
            callback_data=f"del_client:{c[0]}"
        ))
    await message.answer("O'chirmoqchi bo'lgan klientni tanlang:", reply_markup=keyboard)

async def delete_client_callback(callback: types.CallbackQuery):
    client_id = int(callback.data.split(":")[1])
    success, error = delete_client(client_id)
    if success:
        await callback.answer("✅ Klient o'chirildi")
        await callback.message.edit_text(f"Klient (ID: {client_id}) o'chirildi.")
    else:
        await callback.answer("❌ Xatolik: " + (error or "Noma'lum xato"), show_alert=True)
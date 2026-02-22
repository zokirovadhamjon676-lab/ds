from aiogram import types
from database.db import get_orders
from openpyxl import Workbook

async def export_orders_excel(message: types.Message):
    orders = get_orders()
    if not orders:
        await message.answer("📭 Buyurtma mavjud emas.")
        return

    wb = Workbook()
    ws = wb.active
    ws.append(["ID", "Klient", "Mahsulot", "Miqdor", "Sana"])

    for row in orders:
        ws.append(row)

    file_path = "orders.xlsx"
    wb.save(file_path)

    with open(file_path, "rb") as file:
        await message.answer_document(file, caption="📊 Buyurtmalar ro‘yxati")
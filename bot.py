import os
import threading
from flask import Flask
from dotenv import load_dotenv
from bale import Bot, InlineKeyboardMarkup, InlineKeyboardButton

# بارگذاری توکن از متغیر محیطی (توکن رو بعداً توی رندر می‌ذاریم)
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 2070801361

# داده‌های ربات (کشورها و آیتم‌ها)
COUNTRIES = ["ایران", "آمریکا", "روسیه", "انگلستان", "آلمان", "فرانسه"]
ITEMS = {
    "مک‌بوک": {"dollar": 160000, "oil": 10, "elec": 50, "ammo": 30, "damage": 200, "defense": 600, "type": "air"},
    "آیفون": {"dollar": 150000, "oil": 10, "elec": 45, "ammo": 25, "damage": 190, "defense": 500, "type": "air"},
}

bot = Bot(TOKEN)

@bot.message(commands=["start"])
async def start_command(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for country in COUNTRIES:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=country, callback_data=f"country:{country}")])
    await message.answer("سلام! به ربات جنگ خوش آمدید. یک کشور را انتخاب کنید:", reply_markup=keyboard)

@bot.callback_query()
async def handle_callback(callback_query):
    data = callback_query.data
    if data.startswith("country:"):
        country = data.split(":")[1]
        items_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for item_name in ITEMS.keys():
            items_keyboard.inline_keyboard.append([InlineKeyboardButton(text=item_name, callback_data=f"item:{item_name}")])
        await callback_query.message.answer(f"شما کشور {country} را انتخاب کردید. حالا یک آیتم بخرید:", reply_markup=items_keyboard)
        await callback_query.answer()
    elif data.startswith("item:"):
        item_name = data.split(":")[1]
        item_info = ITEMS.get(item_name)
        if item_info:
            text = f"آیتم: {item_name}\nقیمت: {item_info['dollar']} دلار\nخسارت: {item_info['damage']}"
            await callback_query.message.answer(text)
            await callback_query.answer()

# بخش مربوط به زنده نگه داشتن سرویس در رندر
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات فعال است!"

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# اجرای همزمان ربات و وب سرور
if name == "__main__":
    threading.Thread(target=run_web_server).start()
    print("ربات در حال اجراست...")
    bot.run()

import os
from flask import Flask, render_template_string, request, redirect, make_response, jsonify, session
import database
import random

app = Flask(__name__)
app.secret_key = "war_game_secret_2026"
ADMIN_PASSWORD = "War_Game9192"

data = database.load_data()
if "countries" not in data:
    data = {"countries": {}, "statements": [], "chat": [], "last_tick": 0, "attacks": {}}
if "attacks" not in data:
    data["attacks"] = {}

COUNTRIES = {
    "آمریکا": "🇺🇸", "چین": "🇨🇳", "ژاپن": "🇯🇵", "آلمان": "🇩🇪",
    "روسیه": "🇷🇺", "انگلستان": "🇬🇧", "فرانسه": "🇫🇷", "هند": "🇮🇳",
    "ایتالیا": "🇮🇹", "برزیل": "🇧🇷", "کانادا": "🇨🇦", "استرالیا": "🇦🇺",
    "یمن": "🇾🇪", "کره شمالی": "🇰🇵", "کره جنوبی": "🇰🇷", "اندونزی": "🇮🇩",
    "عربستان": "🇸🇦", "ترکیه": "🇹🇷", "ایران": "🇮🇷", "مصر": "🇪🇬",
    "نیجریه": "🇳🇬", "مکزیک": "🇲🇽", "اسپانیا": "🇪🇸", "پاکستان": "🇵🇰",
    "آرژانتین": "🇦🇷", "هلند": "🇳🇱", "سنگاپور": "🇸🇬", "سوئیس": "🇨🇭",
    "امارات": "🇦🇪", "قطر": "🇶🇦", "اسرائیل": "🇮🇱", "کویت": "🇰🇼",
    "اردن": "🇯🇴", "لبنان": "🇱🇧", "سوریه": "🇸🇾", "عراق": "🇮🇶",
    "یونان": "🇬🇷", "پرتغال": "🇵🇹", "سوئد": "🇸🇪", "دانمارک": "🇩🇰",
    "نروژ": "🇳🇴", "فنلاند": "🇫🇮", "اتریش": "🇦🇹", "بلژیک": "🇧🇪",
    "اوکراین": "🇺🇦", "لهستان": "🇵🇱", "رومانی": "🇷🇴", "افغانستان": "🇦🇫",
    "ویتنام": "🇻🇳", "تایلند": "🇹🇭", "مالزی": "🇲🇾", "فیلیپین": "🇵🇭",
    "آفریقای جنوبی": "🇿🇦", "کنیا": "🇰🇪", "شیلی": "🇨🇱", "پرو": "🇵🇪",
    "کلمبیا": "🇨🇴", "ونزوئلا": "🇻🇪", "کوبا": "🇨🇺", "ایرلند": "🇮🇪",
    "قبرس": "🇨🇾", "صربستان": "🇷🇸", "کرواسی": "🇭🇷", "لیبی": "🇱🇾",
    "مغولستان": "🇲🇳", "نپال": "🇳🇵",
    "شوروی": "💀", "آلمان نازی": "🚩", "هخامنشیان": "👑",
    "داعش": "🏴", "القاعده": "🏁", "مالک": "👤"
}

NATIONS_BONUS = {
    "آلمان": {"tank_power": 1.2}, "آمریکا": {"build_speed": 0.8},
    "شوروی": {"manpower_regen": 1.3}, "انگلستان": {"navy_power": 1.2},
    "ژاپن": {"research_speed": 1.15}, "ایتالیا": {"movement_speed": 1.1},
    "فرانسه": {"defense_bonus": 1.2}, "چین": {"manpower_regen": 1.5},
    "برزیل": {"food_production": 1.2}, "کانادا": {"resource_gain": 1.1},
    "استرالیا": {"air_force_power": 1.15}, "هند": {"population_growth": 1.2},
    "ترکیه": {"army_upkeep_reduction": 0.9}, "ایران": {"oil_production": 1.3},
    "مصر": {"trade_bonus": 1.2}, "مکزیک": {"construction_discount": 0.9},
    "اسپانیا": {"diplomacy_bonus": 1.1}, "سوئد": {"tech_discount": 0.85},
    "لهستان": {"infantry_power": 1.2}, "آفریقای جنوبی": {"mining_efficiency": 1.25},
}

BUILDINGS = {
    "معدن اورانیوم": {"price": 100000, "type": "production", "income": "2 اورانیوم"},
    "پالایشگاه نفت": {"price": 100000, "type": "production", "income": "50 نفت"},
    "کارخونه اسلحه": {"price": 100000, "type": "production", "income": "50 اسلحه"},
    "معدن طلا": {"price": 100000, "type": "production", "income": "2 طلا"},
    "شهر": {"price": 100000, "type": "production", "income": "100000 دلار"},
    "معدن آهن": {"price": 100000, "type": "production", "income": "50 فولاد"},
    "بیمارستان": {"price": 100000, "type": "general"},
    "پایگاه پلیس": {"price": 100000, "type": "general"},
    "سد": {"price": 100000, "type": "general"},
    "سامانه پدافند هوایی": {"price": 200000, "type": "defense", "defense": 800},
    "موشک ضد هوایی": {"price": 150000, "type": "defense", "defense": 500},
    "توپ ضد هوایی": {"price": 100000, "type": "defense", "defense": 300},
}

UNITS = {
    "تانک ابرامز": {"price": 500000, "power": 800, "defense": 600, "type": "ground"},
    "تانک تی14 ارماتا": {"price": 550000, "power": 850, "defense": 700, "type": "ground"},
    "تانک لئوپارد": {"price": 480000, "power": 780, "defense": 620, "type": "ground"},
    "تانک چلنجر": {"price": 470000, "power": 760, "defense": 650, "type": "ground"},
    "تانک تایپ99": {"price": 460000, "power": 740, "defense": 630, "type": "ground"},
    "تانک پوکجان": {"price": 300000, "power": 500, "defense": 450, "type": "ground"},
    "تانک کرار": {"price": 280000, "power": 480, "defense": 420, "type": "ground"},
    "سرباز عادی": {"price": 5000, "power": 50, "defense": 30, "type": "ground"},
    "سرباز تکاور": {"price": 12000, "power": 120, "defense": 80, "type": "ground"},
    "سرباز ارپیجی": {"price": 15000, "power": 200, "defense": 60, "type": "ground"},
    "سرباز اسنایپر": {"price": 18000, "power": 250, "defense": 40, "type": "ground"},
    "کماندو": {"price": 25000, "power": 300, "defense": 150, "type": "ground"},
    "لانچر LGM-HOPML": {"price": 400000, "power": 900, "defense": 100, "type": "ground"},
    "لانچر SERMET-ROY": {"price": 380000, "power": 850, "defense": 120, "type": "ground"},
    "لانچر HQ-ETY21": {"price": 420000, "power": 950, "defense": 90, "type": "ground"},
    "لانچر IL-GONDEY": {"price": 350000, "power": 800, "defense": 110, "type": "ground"},
    "لانچر CHL-V56": {"price": 360000, "power": 820, "defense": 100, "type": "ground"},
    "بمب افکن بلک برد": {"price": 2000000, "power": 3000, "defense": 500, "type": "air"},
    "بمب افکن بی دو": {"price": 1800000, "power": 2800, "defense": 450, "type": "air"},
    "بمب افکن اچ20": {"price": 1500000, "power": 2500, "defense": 400, "type": "air"},
    "بمب افکن دورینه": {"price": 1200000, "power": 2200, "defense": 350, "type": "air"},
    "بمب افکن تی یو 160": {"price": 1900000, "power": 2900, "defense": 480, "type": "air"},
    "جنگنده اف 35": {"price": 1000000, "power": 1200, "defense": 800, "type": "air"},
    "جنگنده سوخو57": {"price": 950000, "power": 1150, "defense": 780, "type": "air"},
    "جنگنده تمپست": {"price": 900000, "power": 1100, "defense": 750, "type": "air"},
    "جنگنده MIG-29": {"price": 700000, "power": 900, "defense": 600, "type": "air"},
    "پهباد SHAHED-238": {"price": 200000, "power": 400, "defense": 150, "type": "air"},
    "ناو هواپیمابر جرالد فورد": {"price": 5000000, "power": 4000, "defense": 3000, "type": "navy"},
    "ناو هواپیمابر فوجیان": {"price": 4500000, "power": 3800, "defense": 2800, "type": "navy"},
    "ناو هواپیمابر ملکه الیزابت": {"price": 4200000, "power": 3600, "defense": 2700, "type": "navy"},
    "ناو هواپیمابر کوزنتسوف": {"price": 3500000, "power": 3200, "defense": 2400, "type": "navy"},
    "ناو هواپیمابر گراف": {"price": 3800000, "power": 3400, "defense": 2500, "type": "navy"},
    "ناوشکن آرلی برک": {"price": 1500000, "power": 1500, "defense": 1200, "type": "navy"},
    "ناوشکن آدمیرال گورشکوف": {"price": 1300000, "power": 1300, "defense": 1100, "type": "navy"},
}

BANNED_WORDS = ["fuck", "shit", "damn", "احمق", "خنگ", "کثافت"]

def filter_chat_message(message):
    if not message: return ""
    for w in BANNED_WORDS:
        message = message.replace(w, "***")
    return message

def get_default_country():
    return {
        "gold": 500000, "oil": 0, "uranium": 0, "steel": 0,
        "fuel": 100, "weapons": 0, "manpower": 100, "elec": 100,
        "buildings": [], "units": {}, "status": "active", "bonus": {},
        "wars_won": 0, "wars_lost": 0, "conquered_by": None,
        "is_player": False
    }

def ensure_country(country, is_player=False):
    if country not in data["countries"]:
        c = get_default_country()
        c["bonus"] = NATIONS_BONUS.get(country, {})
        c["is_player"] = is_player
        data["countries"][country] = c
        database.save_data(data)
    elif is_player:
        data["countries"][country]["is_player"] = True
        database.save_data(data)

def is_conquered(country):
    return data["countries"].get(country, {}).get("conquered_by") is not None

def is_player_country(country):
    return data["countries"].get(country, {}).get("is_player", False)

def calculate_army_power(country):
    total = 0
    units = data["countries"].get(country, {}).get("units", {})
    for u, count in units.items():
        unit = UNITS.get(u, {})
        power = unit.get("power", 0) * count
        if unit.get("type") == "ground":
            power *= data["countries"][country].get("bonus", {}).get("infantry_power", 1.0)
            power *= data["countries"][country].get("bonus", {}).get("tank_power", 1.0)
        elif unit.get("type") == "air":
            power *= data["countries"][country].get("bonus", {}).get("air_force_power", 1.0)
        elif unit.get("type") == "navy":
            power *= data["countries"][country].get("bonus", {}).get("navy_power", 1.0)
        total += power
    return int(total)

def calculate_defense_power(country):
    total = 0
    units = data["countries"].get(country, {}).get("units", {})
    for u, count in units.items():
        unit = UNITS.get(u, {})
        total += unit.get("defense", 0) * count
    total *= data["countries"][country].get("bonus", {}).get("defense_bonus", 1.0)
    return int(total)

def calculate_air_defense(country):
    total = 0
    for b in data["countries"].get(country, {}).get("buildings", []):
        if b in BUILDINGS and BUILDINGS[b].get("type") == "defense":
            total += BUILDINGS[b].get("defense", 0)
    return total

def calculate_air_power(country):
    total = 0
    units = data["countries"].get(country, {}).get("units", {})
    for u, count in units.items():
        if UNITS.get(u, {}).get("type") == "air":
            total += UNITS[u]["power"] * count
    return total

@app.route('/')
def home():
    selected = request.cookies.get('country')
    if selected in COUNTRIES and selected in data["countries"]:
        return redirect(f'/dashboard/{selected}')
    
    countries_html = ""
    for country, flag in COUNTRIES.items():
        conquered = is_conquered(country)
        taken = is_player_country(country)
        
        if conquered:
            status_icon = "🔥"
            style = "background:#7f1d1d;opacity:0.7"
        elif taken:
            status_icon = "✅"
            style = "background:#166534"
        else:
            status_icon = ""
            style = "background:#34495e"
        
        countries_html += f'<a href="/set_country/{country}" style="{style};padding:7px;border-radius:5px;text-decoration:none;color:white;font-size:12px;display:block">{flag} {country} {status_icon}</a>'
    
    html = f"""
    <div style="font-family:Tahoma;text-align:center;padding:20px;background:#2c3e50;min-height:100vh;color:white">
        <h1>🌍 جنگ جهانی</h1>
        <h3>یک کشور انتخاب کنید</h3>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:5px;max-width:1100px;margin:auto">
            {countries_html}
        </div>
        <div style="margin-top:40px">
            <a href="/admin" style="color:#4a5568;font-size:11px;text-decoration:none">🔧 پنل مدیریت</a>
        </div>
    </div>
    """
    return html

@app.route('/set_country/<country>')
def set_country(country):
    if country not in COUNTRIES: return "کشور نیست!", 404
    if is_conquered(country): return f"<h2 style='text-align:center;font-family:Tahoma;padding:50px'>این کشور فتح شده است! 🔥 <a href='/'>بازگشت</a></h2>"
    ensure_country(country, is_player=True)
    resp = make_response(redirect(f'/dashboard/{country}'))
    resp.set_cookie('country', country)
    return resp

@app.route('/dashboard/<country>')
def dashboard(country):
    if country not in COUNTRIES: return "کشور نیست!", 404
    ensure_country(country, is_player=True)
    flag = COUNTRIES[country]
    d = data["countries"][country]
    html = """
    <div style="font-family:Tahoma;text-align:center;padding:20px;background:#2c3e50;min-height:100vh;color:white">
        <h1>{{ flag }} منوی {{ country }}</h1>
        <p>💰 طلا: {{ d.gold }} | 🏆 برد: {{ d.wars_won }} | 💀 باخت: {{ d.wars_lost }}</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;max-width:700px;margin:auto">
            <a href="/status/{{ country }}" style="background:#34495e;padding:25px;border-radius:10px;text-decoration:none;color:white;font-size:18px">📊 وضعیت</a>
            <a href="/shop/{{ country }}" style="background:#34495e;padding:25px;border-radius:10px;text-decoration:none;color:white;font-size:18px">🛒 فروشگاه</a>
            <a href="/my_army/{{ country }}" style="background:#34495e;padding:25px;border-radius:10px;text-decoration:none;color:white;font-size:18px">🪖 ارتش من</a>
            <a href="/chat" style="background:#007bff;color:white;padding:25px;border-radius:10px;text-decoration:none;font-size:18px">💬 چت</a>
            <a href="/create_statement/{{ country }}" style="background:#ffc107;color:#333;padding:25px;border-radius:10px;text-decoration:none;font-size:18px">📜 بیانیه</a>
            <a href="/statements" style="background:#28a745;color:white;padding:25px;border-radius:10px;text-decoration:none;font-size:18px">📰 بیانیه‌ها</a>
            <a href="/war/{{ country }}" style="background:#c0392b;color:white;padding:25px;border-radius:10px;text-decoration:none;font-size:18px">⚔️ جنگ</a>
            <a href="/map/{{ country }}" style="background:#8e44ad;color:white;padding:25px;border-radius:10px;text-decoration:none;font-size:18px">🗺️ نقشه</a>
        </div>
    </div>
    """
    return render_template_string(html, country=country, flag=flag, d=d)

@app.route('/status/<country>')
def status(country):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country, is_player=True)
    d = data["countries"][country]
    f = COUNTRIES[country]
    power = calculate_army_power(country)
    defense = calculate_defense_power(country)
    air_def = calculate_air_defense(country)
    return f"""<div style='font-family:Tahoma;text-align:center;padding:40px;background:#2c3e50;min-height:100vh;color:white'>
    <h1>{f} وضعیت {country}</h1>
    <p>💰 طلا: {d.get('gold',0)}</p>
    <p>🛢 نفت: {d.get('oil',0)}</p>
    <p>☢️ اورانیوم: {d.get('uranium',0)}</p>
    <p>🔩 فولاد: {d.get('steel',0)}</p>
    <p>⛽ سوخت: {d.get('fuel',0)}</p>
    <p>🔫 اسلحه: {d.get('weapons',0)}</p>
    <p>👥 نیروی انسانی: {d.get('manpower',0)}</p>
    <p>⚡ برق: {d.get('elec',0)}</p>
    <p>💪 قدرت حمله: {power}</p>
    <p>🛡️ قدرت دفاع: {defense}</p>
    <p>🚀 پدافند هوایی: {air_def}</p>
    <p>🏆 بردها: {d.get('wars_won',0)} | 💀 باخت‌ها: {d.get('wars_lost',0)}</p>
    <p>🏭 ساختمان‌ها: {len(d.get('buildings',[]))}</p>
    <br><a href='/dashboard/{country}' style='color:#ffc107'>بازگشت</a></div>"""

@app.route('/shop/<country>')
def shop(country):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country, is_player=True)
    f = COUNTRIES[country]
    d = data["countries"][country]
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>فروشگاه</title>
    <style>
        body { font-family:Tahoma; background:#2c3e50; color:white; padding:20px; min-height:100vh; }
        .cat { background:rgba(0,0,0,0.4); padding:20px; border-radius:10px; max-width:900px; margin:20px auto; }
        h2 { color:#ffc107; text-align:center; }
        .item { background:#34495e; margin:8px; padding:12px; border-radius:5px; display:flex; justify-content:space-between; align-items:center; gap:10px; }
        .item-name { flex-grow:1; }
        .qty-input { width:60px; padding:5px; border-radius:4px; border:none; text-align:center; }
        .buy-btn { background:#28a745; color:white; padding:8px 15px; border:none; border-radius:5px; cursor:pointer; font-weight:bold; }
        .back { color:#ffc107; display:block; margin:20px; text-align:center; }
    </style></head><body>
        <h1 style="text-align:center">{{ flag }} فروشگاه</h1>
        <p style="text-align:center">💰 موجودی: {{ gold }} طلا</p>
        <div class="cat"><h2>🏭 تولیدی (۱۰۰,۰۰۰ طلا)</h2>
        {% for n, i in items.items() if i.type == 'production' %}
            <div class="item"><span class="item-name">{{ n }} | {{ i.price }} طلا | درآمد: {{ i.income }}</span>
            <form action="/buy/{{ country }}/{{ n }}" method="POST" style="display:flex;gap:5px">
                <input type="number" name="qty" value="1" min="1" class="qty-input">
                <button type="submit" class="buy-btn">🛒 خرید</button>
            </form></div>
        {% endfor %}</div>
        <div class="cat"><h2>🏥 عمومی (۱۰۰,۰۰۰ طلا)</h2>
        {% for n, i in items.items() if i.type == 'general' %}
            <div class="item"><span class="item-name">{{ n }} | {{ i.price }} طلا</span>
            <form action="/buy/{{ country }}/{{ n }}" method="POST" style="display:flex;gap:5px">
                <input type="number" name="qty" value="1" min="1" class="qty-input">
                <button type="submit" class="buy-btn">🛒 خرید</button>
            </form></div>
        {% endfor %}</div>
        <div class="cat"><h2>🛡️ پدافند</h2>
        {% for n, i in items.items() if i.type == 'defense' %}
            <div class="item"><span class="item-name">{{ n }} | {{ i.price }} طلا | دفاع: {{ i.defense }}</span>
            <form action="/buy/{{ country }}/{{ n }}" method="POST" style="display:flex;gap:5px">
                <input type="number" name="qty" value="1" min="1" class="qty-input">
                <button type="submit" class="buy-btn">🛒 خرید</button>
            </form></div>
        {% endfor %}</div>
        <div class="cat"><h2>🪖 نیروی زمینی</h2>
        {% for n, i in units.items() if i.type == 'ground' %}
            <div class="item"><span class="item-name">{{ n }} | {{ i.price }} طلا | 💪 {{ i.power }} | 🛡️ {{ i.defense }}</span>
            <form action="/buy_unit/{{ country }}/{{ n }}" method="POST" style="display:flex;gap:5px">
                <input type="number" name="qty" value="1" min="1" class="qty-input">
                <button type="submit" class="buy-btn">🛒 خرید</button>
            </form></div>
        {% endfor %}</div>
        <div class="cat"><h2>✈️ نیروی هوایی</h2>
        {% for n, i in units.items() if i.type == 'air' %}
            <div class="item"><span class="item-name">{{ n }} | {{ i.price }} طلا | 💪 {{ i.power }} | 🛡️ {{ i.defense }}</span>
            <form action="/buy_unit/{{ country }}/{{ n }}" method="POST" style="display:flex;gap:5px">
                <input type="number" name="qty" value="1" min="1" class="qty-input">
                <button type="submit" class="buy-btn">🛒 خرید</button>
            </form></div>
        {% endfor %}</div>
        <div class="cat"><h2>🚢 نیروی دریایی</h2>
        {% for n, i in units.items() if i.type == 'navy' %}
            <div class="item"><span class="item-name">{{ n }} | {{ i.price }} طلا | 💪 {{ i.power }} | 🛡️ {{ i.defense }}</span>
            <form action="/buy_unit/{{ country }}/{{ n }}" method="POST" style="display:flex;gap:5px">
                <input type="number" name="qty" value="1" min="1" class="qty-input">
                <button type="submit" class="buy-btn">🛒 خرید</button>
            </form></div>
        {% endfor %}</div>
        <a href="/dashboard/{{ country }}" class="back">بازگشت به منو</a>
    </body></html>
    """
    return render_template_string(html, country=country, flag=f, items=BUILDINGS, units=UNITS, gold=d.get("gold", 0))

@app.route('/buy/<country>/<item>', methods=['POST'])
def buy(country, item):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country, is_player=True)
    b = BUILDINGS.get(item)
    if not b: return "آیتم نامعتبر"
    try: qty = int(request.form.get('qty', 1))
    except: qty = 1
    if qty < 1: qty = 1
    total = b.get("price", 0) * qty
    if data["countries"][country]["gold"] < total:
        return f"""<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'>
        <h2>❌ منابع کافی نداری!</h2><p>نیاز: {total} طلا | موجودی: {data["countries"][country]["gold"]} طلا</p>
        <a href='/shop/{country}' style='color:#ffc107'>بازگشت</a></div>"""
    data["countries"][country]["gold"] -= total
    for _ in range(qty): data["countries"][country]["buildings"].append(item)
    database.save_data(data)
    return redirect(f'/shop/{country}')

@app.route('/buy_unit/<country>/<unit_key>', methods=['POST'])
def buy_unit(country, unit_key):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country, is_player=True)
    u = UNITS.get(unit_key)
    if not u: return "واحد نامعتبر"
    try: qty = int(request.form.get('qty', 1))
    except: qty = 1
    if qty < 1: qty = 1
    total = u.get("price", 0) * qty
    if data["countries"][country]["gold"] < total:
        return f"""<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'>
        <h2>❌ منابع کافی نداری!</h2><p>نیاز: {total} طلا | موجودی: {data["countries"][country]["gold"]} طلا</p>
        <a href='/shop/{country}' style='color:#ffc107'>بازگشت</a></div>"""
    data["countries"][country]["gold"] -= total
    units = data["countries"][country].get("units", {})
    units[unit_key] = units.get(unit_key, 0) + qty
    data["countries"][country]["units"] = units
    database.save_data(data)
    return redirect(f'/my_army/{country}')

@app.route('/my_army/<country>')
def my_army(country):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country, is_player=True)
    d = data["countries"][country]
    power = calculate_army_power(country)
    defense = calculate_defense_power(country)
    html = """
    <div style="font-family:Tahoma;background:#2c3e50;min-height:100vh;color:white;padding:20px;text-align:center">
        <h1>🪖 ارتش {{ country }}</h1>
        <p>💪 قدرت حمله: {{ power }} | 🛡️ قدرت دفاع: {{ defense }}</p>
        <div style="background:rgba(0,0,0,0.4);padding:20px;border-radius:10px;max-width:700px;margin:auto">
            <h2>سربازان و تجهیزات</h2>
            {% if d.units %}{% for u, c in d.units.items() %}<p>{{ u }}: {{ c }} عدد</p>{% endfor %}{% else %}<p>هنوز چیزی نداری!</p>{% endif %}
            <h2>ساختمان‌ها</h2>
            {% if d.buildings %}{% for b in d.buildings %}<p>🏭 {{ b }}</p>{% endfor %}{% else %}<p>هنوز ساختمانی نساختی!</p>{% endif %}
        </div>
        <a href="/dashboard/{{ country }}" style="color:#ffc107;display:block;margin-top:20px">بازگشت</a>
    </div>
    """
    return render_template_string(html, country=country, d=d, power=power, defense=defense)

@app.route('/war/<country>')
def war(country):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country, is_player=True)
    my_power = calculate_army_power(country)
    my_defense = calculate_defense_power(country)
    my_air = calculate_air_power(country)
    
    countries_list = []
    for c, f in COUNTRIES.items():
        if c == country: continue
        conquered = is_conquered(c)
        if not conquered and not is_player_country(c):
            continue
        countries_list.append({
            "name": c, "flag": f,
            "power": calculate_army_power(c),
            "defense": calculate_defense_power(c),
            "air": calculate_air_power(c),
            "gold": data["countries"].get(c, {}).get("gold", 0),
            "attacks": data["attacks"].get(country, {}).get(c, 0),
            "conquered": conquered
        })
    
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>جنگ</title>
    <style>
        body { font-family:Tahoma; background:#2c3e50; color:white; text-align:center; padding:20px; min-height:100vh; }
        .my-info { background:rgba(0,0,0,0.5); padding:20px; border-radius:10px; max-width:900px; margin:auto; }
        .country-card { background:#34495e; margin:8px; padding:15px; border-radius:8px; display:flex; justify-content:space-between; align-items:center; gap:10px; }
        .country-card.conquered { background:#7f1d1d; opacity:0.6; }
        .attack-btn { background:#c0392b; color:white; padding:10px 15px; border-radius:5px; text-decoration:none; font-weight:bold; font-size:13px; }
        .air-btn { background:#3498db; color:white; padding:10px 15px; border-radius:5px; text-decoration:none; font-weight:bold; font-size:13px; }
        a { color:#ffc107; }
    </style></head><body>
        <h1>⚔️ مرکز فرماندهی جنگ</h1>
        <div class="my-info">
            <h2>{{ flag }} {{ country }}</h2>
            <p>💪 حمله: <b>{{ my_power }}</b> | 🛡️ دفاع: <b>{{ my_defense }}</b> | ✈️ هوایی: <b>{{ my_air }}</b></p>
            <p>💰 طلا: <b>{{ my_gold }}</b></p>
        </div>
        <h2 style="margin-top:30px">🎯 هدف (۱۵ حمله = فتح)</h2>
        {% if countries_list|length == 0 %}
            <p style="color:#95a5a6">هنوز هیچ کشور دیگه‌ای توسط بازیکن انتخاب نشده!</p>
        {% endif %}
        <div style="max-width:900px;margin:auto">
        {% for c in countries_list %}
            <div class="country-card {% if c.conquered %}conquered{% endif %}">
                <div style="text-align:right;flex-grow:1">
                    <b>{{ c.flag }} {{ c.name }} {% if c.conquered %}🔥{% endif %}</b><br>
                    <small>💪 {{ c.power }} | 🛡️ {{ c.defense }} | ✈️ {{ c.air }} | 💰 {{ c.gold }}</small><br>
                    <small style="color:#f39c12">حملات: {{ c.attacks }}/۱۵</small>
                </div>
                {% if not c.conquered %}
                    <a href="/attack/{{ country }}/{{ c.name }}" class="attack-btn" onclick="return confirm('حمله؟')">⚔️ حمله</a>
                    <a href="/air_attack/{{ country }}/{{ c.name }}" class="air-btn" onclick="return confirm('حمله هوایی؟')">✈️ هوایی</a>
                {% endif %}
            </div>
        {% endfor %}
        </div>
        <a href="/dashboard/{{ country }}" style="display:block;margin-top:30px">بازگشت</a>
    </body></html>
    """
    return render_template_string(html, country=country, flag=COUNTRIES[country], 
                                  my_power=my_power, my_defense=my_defense, my_air=my_air,
                                  my_gold=data["countries"][country].get("gold", 0),
                                  countries_list=countries_list)

@app.route('/attack/<attacker>/<defender>')
def attack(attacker, defender):
    global data
    if attacker not in COUNTRIES or defender not in COUNTRIES: return "کشور نامعتبر", 404
    if is_conquered(defender): return f"<h2 style='text-align:center;font-family:Tahoma;padding:50px'>فتح شده! <a href='/war/{attacker}'>بازگشت</a></h2>"
    
    atk_power = calculate_army_power(attacker)
    def_power = calculate_defense_power(defender)
    atk_roll = atk_power * random.uniform(0.9, 1.1)
    def_roll = def_power * random.uniform(0.9, 1.1)
    
    if attacker not in data["attacks"]: data["attacks"][attacker] = {}
    count = data["attacks"][attacker].get(defender, 0) + 1
    data["attacks"][attacker][defender] = count
    
    if atk_roll > def_roll:
        loot = int(data["countries"][defender].get("gold", 0) * 0.1)
        data["countries"][attacker]["gold"] = data["countries"][attacker].get("gold", 0) + loot
        data["countries"][defender]["gold"] = data["countries"][defender].get("gold", 0) - loot
        def_units = data["countries"][defender].get("units", {})
        for u in list(def_units.keys()):
            if def_units[u] > 0: def_units[u] = max(0, def_units[u] - random.randint(1, 3))
        data["countries"][defender]["units"] = def_units
        won = True
        message = f"⚔️ حمله {count}/۱۵ موفق! {loot} طلا غنیمت."
    else:
        atk_units = data["countries"][attacker].get("units", {})
        for u in list(atk_units.keys()):
            if atk_units[u] > 0: atk_units[u] = max(0, atk_units[u] - random.randint(1, 3))
        data["countries"][attacker]["units"] = atk_units
        won = False
        message = f"💀 حمله {count}/۱۵ شکست خورد!"
    
    conquered = False
    if count >= 15:
        data["countries"][defender]["conquered_by"] = attacker
        data["countries"][attacker]["wars_won"] = data["countries"][attacker].get("wars_won", 0) + 1
        data["countries"][defender]["wars_lost"] = data["countries"][defender].get("wars_lost", 0) + 1
        conquered = True
        message += f" 🔥 {defender} فتح شد!"
    
    database.save_data(data)
    color = "#28a745" if won else "#c0392b"
    extra = "<p style='font-size:24px'>🔥🔥🔥 فتح شد! 🔥🔥🔥</p>" if conquered else ""
    return f"""<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'>
    <h1 style='color:{color}'>{message}</h1>{extra}
    <p>قدرت تو: {int(atk_roll)} | دشمن: {int(def_roll)}</p>
    <a href='/war/{attacker}' style='color:#ffc107'>ادامه</a> | <a href='/dashboard/{attacker}' style='color:#ffc107'>منو</a></div>"""

@app.route('/air_attack/<attacker>/<defender>')
def air_attack(attacker, defender):
    global data
    if attacker not in COUNTRIES or defender not in COUNTRIES: return "نامعتبر", 404
    if is_conquered(defender): return f"<h2 style='text-align:center;font-family:Tahoma;padding:50px'>فتح شده! <a href='/war/{attacker}'>بازگشت</a></h2>"
    
    air_power = calculate_air_power(attacker)
    air_defense = calculate_air_defense(defender)
    if air_power <= 0: return f"<h2 style='text-align:center;font-family:Tahoma;padding:50px'>✈️ نیروی هوایی نداری! <a href='/war/{attacker}'>بازگشت</a></h2>"
    
    effective_air = air_power * (1 - air_defense / (air_defense + air_power + 1))
    damage = int(effective_air / 500)
    
    production = [b for b in data["countries"][defender].get("buildings", []) if b in BUILDINGS and BUILDINGS[b].get("type") == "production"]
    destroyed = []
    for _ in range(min(damage, len(production))):
        if production:
            b = production.pop(random.randint(0, len(production) - 1))
            data["countries"][defender]["buildings"].remove(b)
            destroyed.append(b)
    
    if air_defense > 0:
        air_units = data["countries"][attacker].get("units", {})
        losses = int(len(destroyed) / 2) + 1
        for u in list(air_units.keys()):
            if UNITS.get(u, {}).get("type") == "air" and air_units[u] > 0:
                air_units[u] = max(0, air_units[u] - random.randint(0, losses))
        data["countries"][attacker]["units"] = air_units
    
    database.save_data(data)
    destroyed_text = "".join([f"<p>💥 {b} نابود شد</p>" for b in destroyed]) if destroyed else "<p>هیچ ساختمانی نابود نشد</p>"
    return f"""<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'>
    <h1>✈️ حمله هوایی به {defender}</h1>
    <p>قدرت هوایی: {air_power} | پدافند دشمن: {air_defense}</p>
    <p>خسارت: {damage}</p>{destroyed_text}
    <a href='/war/{attacker}' style='color:#ffc107'>بازگشت</a></div>"""

@app.route('/chat')
def chat():
    country = request.cookies.get('country', '')
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>چت</title>
    <style>
        body { margin:0; padding:0; background:#2c3e50; font-family:Tahoma; min-height:100vh; }
        .chat-container { position:fixed; bottom:20px; left:20px; width:380px; height:280px; background:rgba(0,0,0,0.85); border:1px solid #444; color:white; display:flex; flex-direction:column; border-radius:8px; }
        .chat-history { flex-grow:1; overflow-y:auto; padding:10px; font-size:13px; }
        .chat-input-area { padding:5px; display:flex; border-top:1px solid #444; }
        .chat-input-area input { flex-grow:1; padding:8px; border:none; background:#333; color:white; border-radius:4px; }
        .chat-input-area button { padding:8px 15px; margin-right:5px; background:#007bff; color:white; border:none; border-radius:4px; cursor:pointer; }
        .back-link { position:absolute; top:10px; right:10px; color:white; background:#333; padding:10px; border-radius:5px; text-decoration:none; }
    </style></head><body>
        <a href="/dashboard/{{ country }}" class="back-link">بازگشت</a>
        <div class="chat-container">
            <div id="chat-history" class="chat-history"></div>
            <div class="chat-input-area">
                <input type="text" id="chat-input" placeholder="پیام...">
                <button onclick="sendMessage()">ارسال</button>
            </div>
        </div>
        <script>
            const ch = document.getElementById('chat-history');
            const ci = document.getElementById('chat-input');
            function sendMessage() {
                if (ci.value.trim() === '') return;
                fetch('/api/send_message', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:ci.value})}).then(()=>{ci.value='';load()});
            }
            function load() {
                fetch('/api/get_messages').then(r=>r.json()).then(d=>{
                    ch.innerHTML = '';
                    d.forEach(m => ch.innerHTML += `<p><b>${m.sender}:</b> ${m.text}</p>`);
                    ch.scrollTop = ch.scrollHeight;
                });
            }
            setInterval(load, 3000); load();
            ci.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });
        </script>
    </body></html>
    """
    return render_template_string(html, country=country)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    global data
    req = request.get_json()
    country = request.cookies.get('country', 'ناشناس')
    msg = filter_chat_message(req.get('message', ''))
    flag = COUNTRIES.get(country, "🏳")
    if msg:
        data["chat"].append({"sender": f"{flag} {country}", "text": msg})
        if len(data["chat"]) > 100: data["chat"] = data["chat"][-100:]
        database.save_data(data)
    return jsonify({"status": "ok"})

@app.route('/api/get_messages')
def get_messages():
    return jsonify(data.get("chat", []))

@app.route('/create_statement/<country>')
def create_statement(country):
    if country not in COUNTRIES: return "کشور نیست"
    flag = COUNTRIES[country]
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>بیانیه</title>
    <style>
        body { font-family:Tahoma; background:#2c3e50; color:white; text-align:center; padding:50px; min-height:100vh; }
        .box { background:rgba(0,0,0,0.6); padding:30px; border-radius:10px; max-width:500px; margin:auto; }
        select, textarea { width:100%; padding:10px; margin:10px 0; border-radius:5px; border:none; font-family:Tahoma; box-sizing:border-box; }
        textarea { height:150px; resize:vertical; }
        button { background:#28a745; color:white; padding:15px 30px; border:none; border-radius:5px; cursor:pointer; font-size:16px; }
        a { color:#ffc107; display:block; margin-top:20px; }
    </style></head><body>
        <div class="box">
            <h1>{{ flag }} بیانیه جدید</h1>
            <form action="/save_statement" method="POST">
                <input type="hidden" name="country" value="{{ country }}">
                <label>خطاب به:</label>
                <select name="target">
                    <option value="به جهان 🌍">به جهان 🌍</option>
                    {% for c, f in countries.items() %}{% if c != country %}<option value="{{ f }} {{ c }}">{{ f }} {{ c }}</option>{% endif %}{% endfor %}
                </select>
                <textarea name="text" placeholder="متن بیانیه..."></textarea>
                <button type="submit">ارسال</button>
            </form>
            <a href="/dashboard/{{ country }}">بازگشت</a>
        </div>
    </body></html>
    """
    return render_template_string(html, country=country, flag=flag, countries=COUNTRIES)

@app.route('/save_statement', methods=['POST'])
def save_statement():
    global data
    country = request.form.get('country'); target = request.form.get('target'); text = request.form.get('text')
    flag = COUNTRIES.get(country, "🏳")
    if country and text:
        data["statements"].append({"country": country, "flag": flag, "target": target, "text": text})
        database.save_data(data)
    return redirect('/statements')

@app.route('/statements')
def view_statements():
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>بیانیه‌ها</title>
    <style>
        body { font-family:Tahoma; background:#2c3e50; color:white; text-align:center; padding:20px; min-height:100vh; }
        .statement { background:rgba(0,0,0,0.6); padding:20px; border-radius:10px; max-width:700px; margin:20px auto; text-align:right; }
        .header { color:#ffc107; font-weight:bold; margin:5px 0; }
        .line { border-top:1px dashed #888; margin:10px 0; }
        .end { color:#28a745; font-weight:bold; text-align:left; }
        a { color:#ffc107; }
    </style></head><body>
        <h1>📰 بیانیه‌ها</h1><a href="/">بازگشت</a>
        {% for s in statements|reverse %}
            <div class="statement">
                <div class="header">کشور: {{ s.flag }} {{ s.country }}</div>
                <div class="header">مورد: بیانیه 🗞</div>
                <div class="header">خطاب: {{ s.target }}</div>
                <div class="line"></div><div style="line-height:1.8">{{ s.text }}</div><div class="line"></div>
                <div class="end">تمام.</div>
            </div>
        {% endfor %}
    </body></html>
    """
    return render_template_string(html, statements=data.get("statements", []))

@app.route('/map/<country>')
def map_view(country):
    return f"""<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'>
    <h1>🗺️ نقشه {country}</h1><a href='/dashboard/{country}' style='color:#ffc107'>بازگشت</a></div>"""

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
        return "رمز اشتباه! <a href='/admin'>تلاش مجدد</a>"
    if not session.get('admin'):
        return """<div style="font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white">
            <h1>ورود ادمین</h1><form method="POST">
            <input type="password" name="password" placeholder="رمز" style="padding:10px;font-size:16px">
            <button type="submit" style="padding:10px 20px;background:#007bff;color:white;border:none;border-radius:5px">ورود</button>
            </form><a href="/" style="color:#ffc107">بازگشت</a></div>"""
    
    countries_rows = ""
    for country, flag in COUNTRIES.items():
        if country in data["countries"] and data["countries"][country].get('is_player', False):
            gold = data["countries"][country].get('gold', 0)
            conquered = "🔥 فتح" if data["countries"][country].get('conquered_by') else "✅ فعال"
            countries_rows += f"""
            <tr>
                <td>{flag} {country}</td>
                <td>{gold}</td>
                <td>{conquered}</td>
                <td>
                    <a href="/admin/fine/{country}" class="btn btn-warning">جریمه ۲۵۰k</a>
                    <a href="/admin/gold/{country}" class="btn btn-success">+ ۱۰۰k</a>
                    <a href="/admin/delete/{country}" class="btn btn-danger" onclick="return confirm('حذف؟')">حذف</a>
                </td>
            </tr>"""
    
    if not countries_rows:
        countries_rows = "<tr><td colspan='4' style='color:#95a5a6'>هنوز هیچ کشوری توسط بازیکن انتخاب نشده.</td></tr>"
    
    chat_rows = ""
    for i, msg in enumerate(data.get("chat", [])):
        sender = msg.get("sender", "")
        text = msg.get("text", "")
        chat_rows += f"""
        <div style="background:#34495e;padding:10px;border-radius:5px;margin:5px 0;display:flex;justify-content:space-between;align-items:center;gap:10px">
            <span style="flex-grow:1;text-align:right"><b>{sender}:</b> {text}</span>
            <a href="/admin/delete_chat/{i}" class="btn btn-danger" onclick="return confirm('حذف پیام؟')">🗑️</a>
        </div>"""
    
    if not chat_rows:
        chat_rows = "<p style='color:#95a5a6'>هیچ پیامی وجود ندارد.</p>"
    
    stmt_rows = ""
    for i, stmt in enumerate(data.get("statements", [])):
        country = stmt.get("country", "")
        flag = stmt.get("flag", "")
        target = stmt.get("target", "")
        text = stmt.get("text", "")
        stmt_rows += f"""
        <div style="background:#34495e;padding:10px;border-radius:5px;margin:5px 0;text-align:right">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span><b>{flag} {country}</b> → <b>{target}</b></span>
                <a href="/admin/delete_statement/{i}" class="btn btn-danger" onclick="return confirm('حذف بیانیه؟')">🗑️</a>
            </div>
            <p style="margin:8px 0;line-height:1.6">{text}</p>
        </div>"""
    
    if not stmt_rows:
        stmt_rows = "<p style='color:#95a5a6'>هیچ بیانیه‌ای وجود ندارد.</p>"
    
    html = f"""
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>ادمین</title>
    <style>
        body {{ font-family:Tahoma; background:#2c3e50; color:white; padding:20px; }}
        .box {{ background:rgba(0,0,0,0.6); padding:20px; border-radius:10px; max-width:1000px; margin:20px auto; }}
        table {{ width:100%; border-collapse:collapse; }}
        th, td {{ padding:8px; border-bottom:1px solid #444; font-size:13px; text-align:center; }}
        .btn {{ padding:5px 8px; border:none; border-radius:5px; color:white; text-decoration:none; font-size:11px; display:inline-block; }}
        .btn-danger {{ background:#dc3545; }} .btn-warning {{ background:#ffc107; color:#333; }} .btn-success {{ background:#28a745; }}
        a {{ color:#ffc107; }}
        h2 {{ color:#ffc107; border-bottom:2px solid #ffc107; padding-bottom:10px; margin-top:30px; }}
    </style></head><body>
        <div class="box">
            <h1 style="text-align:center">🛡️ پنل ادمین</h1>
            
            <h2>🌍 مدیریت کشورها</h2>
            <table>
                <tr><th>کشور</th><th>طلا</th><th>وضعیت</th><th>عملیات</th></tr>
                {countries_rows}
            </table>
            
            <h2>💬 مدیریت چت ({len(data.get('chat', []))} پیام)</h2>
            {chat_rows}
            
            <h2>📰 مدیریت بیانیه‌ها ({len(data.get('statements', []))} بیانیه)</h2>
            {stmt_rows}
            
            <br><div style="text-align:center;margin-top:20px"><a href="/">بازگشت به خانه</a> | <a href="/admin/logout">خروج از ادمین</a></div>
        </div>
    </body></html>
    """
    return html

@app.route('/admin/delete_chat/<int:index>')
def admin_delete_chat(index):
    if not session.get('admin'): return redirect('/admin')
    if 0 <= index < len(data["chat"]):
        del data["chat"][index]
        database.save_data(data)
    return redirect('/admin')

@app.route('/admin/delete_statement/<int:index>')
def admin_delete_statement(index):
    if not session.get('admin'): return redirect('/admin')
    if 0 <= index < len(data["statements"]):
        del data["statements"][index]
        database.save_data(data)
    return redirect('/admin')

@app.route('/admin/fine/<country>')
def admin_fine(country):
    if not session.get('admin'): return redirect('/admin')
    if country in data["countries"]:
        data["countries"][country]["gold"] -= 250000
        database.save_data(data)
    return redirect('/admin')

@app.route('/admin/gold/<country>')
def admin_gold(country):
    if not session.get('admin'): return redirect('/admin')
    if country in data["countries"]:
        data["countries"][country]["gold"] += 100000
        database.save_data(data)
    return redirect('/admin')

@app.route('/admin/delete/<country>')
def admin_delete(country):
    if not session.get('admin'): return redirect('/admin')
    if country in data["countries"]:
        del data["countries"][country]
        database.save_data(data)
    return redirect('/admin')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/reset')
def reset():
    resp = make_response(redirect('/'))
    resp.delete_cookie('country')
    return resp

port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port)
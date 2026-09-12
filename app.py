import os
from flask import Flask, render_template_string, request, redirect, make_response, jsonify, session
import database

app = Flask(__name__)
app.secret_key = "war_game_secret_2026"
ADMIN_PASSWORD = "War_Game9192"

# ============================================================
# بارگذاری دیتابیس از گیت‌هاب
# ============================================================
data = database.load_data()
if "countries" not in data:
    data = {"countries": {}, "statements": [], "chat": [], "last_tick": 0}

# ============================================================
# لیست کشورها با پرچم
# ============================================================
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
    "لوکزامبورگ": "🇱🇺", "چک": "🇨🇿", "لهستان": "🇵🇱", "مجارستان": "🇭🇺",
    "رومانی": "🇷🇴", "بلغارستان": "🇧🇬", "اوکراین": "🇺🇦", "بلاروس": "🇧🇾",
    "گرجستان": "🇬🇪", "آذربایجان": "🇦🇿", "ارمنستان": "🇦🇲", "ازبکستان": "🇺🇿",
    "تاجیکستان": "🇹🇯", "قرقیزستان": "🇰🇬", "ترکمنستان": "🇹🇲", "افغانستان": "🇦🇫",
    "سریلانکا": "🇱🇰", "میانمار": "🇲🇲", "ویتنام": "🇻🇳", "تایلند": "🇹🇭",
    "مالزی": "🇲🇾", "فیلیپین": "🇵🇭", "کامبوج": "🇰🇭", "لائوس": "🇱🇦",
    "آفریقای جنوبی": "🇿🇦", "کنیا": "🇰🇪", "اتیوپی": "🇪🇹", "کنگو": "🇨🇩",
    "کامرون": "🇨🇲", "آنگولا": "🇦🇴", "موزامبیک": "🇲🇿", "غنا": "🇬🇭",
    "ساحل عاج": "🇨🇮", "سودان": "🇸🇩", "تانزانیا": "🇹🇿", "اوگاندا": "🇺🇬",
    "زیمبابوه": "🇿🇼", "زامبیا": "🇿🇲", "شیلی": "🇨🇱", "پرو": "🇵🇪",
    "کلمبیا": "🇨🇴", "ونزوئلا": "🇻🇪", "گویان": "🇬🇾", "اروگوئه": "🇺🇾",
    "پاراگوئه": "🇵🇾", "کوبا": "🇨🇺", "دومینیکن": "🇩🇴", "هائیتی": "🇭🇹",
    "جامائیکا": "🇯🇲", "باربادوس": "🇧🇧", "گرنادا": "🇬🇩", "سنت لوسیا": "🇱🇨",
    "وینست": "🇻🇨", "آنتیگوا": "🇦🇬", "باهاما": "🇧🇸", "دومینیکا": "🇩🇲",
    "سنت مالکو": "🇰🇳", "ایرلند": "🇮🇪", "مالت": "🇲🇹", "قبرس": "🇨🇾",
    "آلبانی": "🇦🇱", "مقدونیه": "🇲🇰", "صربستان": "🇷🇸", "کرواسی": "🇭🇷",
    "اسلوونی": "🇸🇮", "هرزگوین": "🇧🇦", "لیبی": "🇱🇾", "مونته‌نگرو": "🇲🇪",
    "آندورا": "🇦🇩", "موناکو": "🇲🇨", "سان مارینو": "🇸🇲", "واتیکان": "🇻🇦",
    "لیختن‌اشتاین": "🇱🇮", "شاش الدوله": "🏳", "دزدان دریایی": "🏴‍☠",
    "داعش": "🏴", "آلمان نازی": "🚩", "القاعده": "🏁",
    "هخامنشیان": "👑", "شوروی": "💀", "مالک": "👤"
}

# ============================================================
# ۲۰ ملیت با بونوس (Game Config از فایل تو)
# ============================================================
NATIONS_BONUS = {
    "آلمان": {"tank_power": 1.2, "name": "آلمان"},
    "آمریکا": {"build_speed": 0.8, "name": "آمریکا"},
    "شوروی": {"manpower_regen": 1.3, "name": "شوروی"},
    "انگلستان": {"navy_power": 1.2, "name": "بریتانیا"},
    "ژاپن": {"research_speed": 1.15, "name": "ژاپن"},
    "ایتالیا": {"movement_speed": 1.1, "name": "ایتالیا"},
    "فرانسه": {"defense_bonus": 1.2, "name": "فرانسه"},
    "چین": {"manpower_regen": 1.5, "name": "چین"},
    "برزیل": {"food_production": 1.2, "name": "برزیل"},
    "کانادا": {"resource_gain": 1.1, "name": "کانادا"},
    "استرالیا": {"air_force_power": 1.15, "name": "استرالیا"},
    "هند": {"population_growth": 1.2, "name": "هند"},
    "ترکیه": {"army_upkeep_reduction": 0.9, "name": "ترکیه"},
    "ایران": {"oil_production": 1.3, "name": "ایران"},
    "مصر": {"trade_bonus": 1.2, "name": "مصر"},
    "مکزیک": {"construction_discount": 0.9, "name": "مکزیک"},
    "اسپانیا": {"diplomacy_bonus": 1.1, "name": "اسپانیا"},
    "سوئد": {"tech_discount": 0.85, "name": "سوئد"},
    "لهستان": {"infantry_power": 1.2, "name": "لهستان"},
    "آفریقای جنوبی": {"mining_efficiency": 1.25, "name": "آفریقای جنوبی"},
}

# ============================================================
# ساختمان‌ها
# ============================================================
BUILDINGS = {
    "mine": {"name": "معدن آهن", "price": 100, "steel_cost": 100, "produce": {"steel": 50}, "type": "production"},
    "refinery": {"name": "پالایشگاه", "price": 150, "steel_cost": 150, "produce": {"fuel": 40}, "type": "production"},
    "barracks": {"name": "پادگان", "price": 200, "steel_cost": 200, "unlock": ["infantry", "light_tank"], "type": "production"},
    "uranium_mine": {"name": "معدن اورانیوم", "price": 100000, "produce": {"uranium": 2}, "type": "production"},
    "gold_mine": {"name": "معدن طلا", "price": 150000, "produce": {"gold": 2}, "type": "production"},
    "city": {"name": "شهر", "price": 250000, "produce": {"gold": 100000}, "type": "production"},
    "hospital": {"name": "بیمارستان", "price": 10000, "type": "general"},
    "police": {"name": "پایگاه پلیس", "price": 10000, "type": "general"},
    "dam": {"name": "سد", "price": 15000, "type": "general"},
}

# ============================================================
# واحدها (از فایل تو)
# ============================================================
UNITS = {
    "infantry": {"name": "سرباز عادی", "price": 5000, "steel_cost": 50, "fuel_cost": 0, "manpower": 10, "upkeep": 1, "power": 10, "type": "ground"},
    "light_tank": {"name": "تانک سبک", "price": 120000, "steel_cost": 150, "fuel_cost": 50, "manpower": 5, "upkeep": 5, "power": 40, "type": "ground"},
    "heavy_tank": {"name": "تانک سنگین", "price": 500000, "steel_cost": 500, "fuel_cost": 200, "manpower": 2, "upkeep": 15, "power": 120, "type": "ground"},
    "artillery": {"name": "توپخانه", "price": 300000, "steel_cost": 300, "fuel_cost": 50, "manpower": 5, "upkeep": 8, "power": 80, "type": "support"},
    "tank_abrams": {"name": "تانک ابرامز", "price": 500000, "upkeep": 20, "power": 800, "defense": 600, "type": "ground"},
    "tank_armata": {"name": "تانک تی14 ارماتا", "price": 550000, "upkeep": 22, "power": 850, "defense": 700, "type": "ground"},
    "tank_leopard": {"name": "تانک لئوپارد", "price": 480000, "upkeep": 18, "power": 780, "defense": 620, "type": "ground"},
    "tank_challenger": {"name": "تانک چلنجر", "price": 470000, "upkeep": 18, "power": 760, "defense": 650, "type": "ground"},
    "tank_type99": {"name": "تانک تایپ99", "price": 460000, "upkeep": 17, "power": 740, "defense": 630, "type": "ground"},
    "soldier_regular": {"name": "سرباز عادی", "price": 5000, "upkeep": 1, "power": 50, "defense": 30, "type": "ground"},
    "soldier_ranger": {"name": "سرباز تکاور", "price": 12000, "upkeep": 2, "power": 120, "defense": 80, "type": "ground"},
    "soldier_rpg": {"name": "سرباز ارپیجی", "price": 15000, "upkeep": 2, "power": 200, "defense": 60, "type": "ground"},
    "soldier_sniper": {"name": "سرباز اسنایپر", "price": 18000, "upkeep": 3, "power": 250, "defense": 40, "type": "ground"},
    "commando": {"name": "کماندو", "price": 25000, "upkeep": 4, "power": 300, "defense": 150, "type": "ground"},
    "bomber_blackbird": {"name": "بمب افکن بلک برد", "price": 2000000, "upkeep": 100, "power": 3000, "defense": 500, "type": "air"},
    "bomber_b2": {"name": "بمب افکن بی دو", "price": 1800000, "upkeep": 90, "power": 2800, "defense": 450, "type": "air"},
    "bomber_h20": {"name": "بمب افکن اچ20", "price": 1500000, "upkeep": 80, "power": 2500, "defense": 400, "type": "air"},
    "bomber_tu160": {"name": "بمب افکن تی یو 160", "price": 1900000, "upkeep": 95, "power": 2900, "defense": 480, "type": "air"},
    "fighter_f35": {"name": "جنگنده اف 35", "price": 1000000, "upkeep": 50, "power": 1200, "defense": 800, "type": "air"},
    "fighter_su57": {"name": "جنگنده سوخو57", "price": 950000, "upkeep": 48, "power": 1150, "defense": 780, "type": "air"},
    "fighter_tempest": {"name": "جنگنده تمپست", "price": 900000, "upkeep": 45, "power": 1100, "defense": 750, "type": "air"},
    "fighter_mig29": {"name": "جنگنده MIG-29", "price": 700000, "upkeep": 35, "power": 900, "defense": 600, "type": "air"},
    "drone_shahed": {"name": "پهباد SHAHED-238", "price": 200000, "upkeep": 10, "power": 400, "defense": 150, "type": "air"},
    "carrier_gerald": {"name": "ناو هواپیمابر جرالد فورد", "price": 5000000, "upkeep": 250, "power": 4000, "defense": 3000, "type": "navy"},
    "carrier_fujian": {"name": "ناو هواپیمابر فوجیان", "price": 4500000, "upkeep": 230, "power": 3800, "defense": 2800, "type": "navy"},
    "carrier_elizabeth": {"name": "ناو هواپیمابر ملکه الیزابت", "price": 4200000, "upkeep": 220, "power": 3600, "defense": 2700, "type": "navy"},
    "carrier_kuznetsov": {"name": "ناو هواپیمابر کوزنتسوف", "price": 3500000, "upkeep": 180, "power": 3200, "defense": 2400, "type": "navy"},
    "carrier_graf": {"name": "ناو هواپیمابر گراف", "price": 3800000, "upkeep": 200, "power": 3400, "defense": 2500, "type": "navy"},
    "destroyer_burke": {"name": "ناوشکن آرلی برک", "price": 1500000, "upkeep": 80, "power": 1500, "defense": 1200, "type": "navy"},
    "destroyer_gorshkov": {"name": "ناوشکن آدمیرال گورشکوف", "price": 1300000, "upkeep": 70, "power": 1300, "defense": 1100, "type": "navy"},
}

# ============================================================
# مختصات نقشه
# ============================================================
MAP_COORDINATES = {
    "آلمان": {"lat": 51.0, "lng": 10.0},
    "آمریکا": {"lat": 37.0, "lng": -95.0},
    "شوروی": {"lat": 60.0, "lng": 90.0},
    "انگلستان": {"lat": 54.0, "lng": -2.0},
    "ژاپن": {"lat": 36.0, "lng": 138.0},
    "ایتالیا": {"lat": 41.0, "lng": 12.0},
    "فرانسه": {"lat": 46.0, "lng": 2.0},
    "چین": {"lat": 35.0, "lng": 105.0},
    "برزیل": {"lat": -10.0, "lng": -55.0},
    "کانادا": {"lat": 56.0, "lng": -106.0},
    "استرالیا": {"lat": -25.0, "lng": 133.0},
    "هند": {"lat": 20.0, "lng": 77.0},
    "ترکیه": {"lat": 39.0, "lng": 35.0},
    "ایران": {"lat": 32.0, "lng": 53.0},
    "مصر": {"lat": 26.0, "lng": 30.0},
    "مکزیک": {"lat": 23.0, "lng": -102.0},
    "اسپانیا": {"lat": 40.0, "lng": -4.0},
    "سوئد": {"lat": 62.0, "lng": 15.0},
    "لهستان": {"lat": 52.0, "lng": 19.0},
    "آفریقای جنوبی": {"lat": -30.0, "lng": 22.0},
}

# ============================================================
# فیلتر کلمات نامناسب
# ============================================================
BANNED_WORDS = ["fuck", "shit", "damn", "احمق", "خنگ", "کثافت"]

def filter_chat_message(message):
    if not message:
        return ""
    filtered = message
    for w in BANNED_WORDS:
        filtered = filtered.replace(w, "***")
    return filtered

# ============================================================
# توابع منطق بازی
# ============================================================
def get_default_country():
    return {
        "gold": 1000000, "oil": 500, "uranium": 10, "steel": 500,
        "fuel": 500, "weapons": 500, "manpower": 1000, "elec": 500,
        "buildings": [], "units": {}, "status": "active", "bonus": {}
    }

def ensure_country(country):
    if country not in data["countries"]:
        c = get_default_country()
        c["bonus"] = NATIONS_BONUS.get(country, {})
        data["countries"][country] = c
        database.save_data(data)

def apply_bonus(country, base_value, bonus_key):
    bonus = data["countries"].get(country, {}).get("bonus", {}).get(bonus_key, 1.0)
    return base_value * bonus

def calculate_upkeep(country):
    total = 0
    units = data["countries"].get(country, {}).get("units", {})
    for u, count in units.items():
        up = UNITS.get(u, {}).get("upkeep", 0)
        total += up * count
    reduction = data["countries"].get(country, {}).get("bonus", {}).get("army_upkeep_reduction", 1.0)
    return int(total * reduction)

def tick_maintenance(country):
    up = calculate_upkeep(country)
    gold = data["countries"][country].get("gold", 0)
    if gold >= up:
        data["countries"][country]["gold"] -= up
        return {"status": "ok", "paid": up}
    else:
        data["countries"][country]["gold"] = 0
        data["countries"][country]["status"] = "inefficient"
        return {"status": "inefficient", "shortage": up - gold}

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

def simulate_combat(attacker, defender):
    atk = calculate_army_power(attacker)
    dfn = calculate_army_power(defender)
    dfn *= data["countries"][defender].get("bonus", {}).get("defense_bonus", 1.0)
    if atk > dfn:
        return {"winner": attacker, "loser": defender, "atk": atk, "dfn": int(dfn)}
    elif dfn > atk:
        return {"winner": defender, "loser": attacker, "atk": atk, "dfn": int(dfn)}
    return {"winner": "مساوی", "loser": None, "atk": atk, "dfn": int(dfn)}

def can_build_unit(country, unit_key):
    unit = UNITS.get(unit_key)
    if not unit: return {"ok": False, "reason": "واحد نامعتبر"}
    if unit["type"] == "ground" and unit_key in ["infantry", "light_tank"]:
        if "barracks" not in data["countries"][country].get("buildings", []):
            return {"ok": False, "reason": "برای ساخت این واحد به پادگان نیاز داری"}
    return {"ok": True}

# ============================================================
# روت‌ها (Routes)
# ============================================================
@app.route('/')
def home():
    selected = request.cookies.get('country')
    if selected in COUNTRIES and selected in data["countries"]:
        return redirect(f'/dashboard/{selected}')
    html = """
    <div style="font-family:Tahoma;text-align:center;padding:20px;background:#2c3e50;min-height:100vh;color:white">
        <h1>🌍 جنگ جهانی</h1>
        <h3>یک کشور انتخاب کنید</h3>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:5px;max-width:1100px;margin:auto">
        {% for country, flag in countries.items() %}
            <a href="/set_country/{{ country }}" style="background:#34495e;padding:7px;border-radius:5px;text-decoration:none;color:white;font-size:12px">{{ flag }} {{ country }}</a>
        {% endfor %}
        </div>
    </div>
    """
    return render_template_string(html, countries=COUNTRIES)

@app.route('/set_country/<country>')
def set_country(country):
    if country not in COUNTRIES: return "کشور نیست!", 404
    ensure_country(country)
    resp = make_response(redirect(f'/dashboard/{country}'))
    resp.set_cookie('country', country)
    return resp

@app.route('/dashboard/<country>')
def dashboard(country):
    if country not in COUNTRIES: return "کشور نیست!", 404
    ensure_country(country)
    flag = COUNTRIES[country]
    d = data["countries"][country]
    bonus = d.get("bonus", {})
    bonus_text = " | ".join([f"{k}: {v}" for k, v in bonus.items() if k != "name"])
    html = """
    <div style="font-family:Tahoma;text-align:center;padding:20px;background:#2c3e50;min-height:100vh;color:white">
        <h1>{{ flag }} منوی {{ country }}</h1>
        {% if bonus_text %}<p style="color:#f39c12">✨ بونوس: {{ bonus_text }}</p>{% endif %}
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
        <a href="/reset" style="display:block;margin-top:20px;color:#e74c3c">تغییر کشور</a>
        <a href="/admin" style="display:block;margin-top:10px;color:#95a5a6;font-size:12px">ورود ادمین</a>
    </div>
    """
    return render_template_string(html, country=country, flag=flag, bonus_text=bonus_text)

@app.route('/status/<country>')
def status(country):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country)
    d = data["countries"][country]
    f = COUNTRIES[country]
    upkeep = calculate_upkeep(country)
    power = calculate_army_power(country)
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
    <p>⚙️ هزینه نگهداری: {upkeep} طلا</p>
    <p>💪 قدرت کل ارتش: {power}</p>
    <p>🏭 ساختمان‌ها: {len(d.get('buildings',[]))}</p>
    <p>وضعیت: {d.get('status','active')}</p>
    <br><a href='/dashboard/{country}' style='color:#ffc107'>بازگشت</a></div>"""

@app.route('/shop/<country>')
def shop(country):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country)
    f = COUNTRIES[country]
    d = data["countries"][country]
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>فروشگاه</title>
    <style>
        body { font-family:Tahoma; background:#2c3e50; color:white; text-align:center; padding:20px; min-height:100vh; }
        .cat { background:rgba(0,0,0,0.4); padding:20px; border-radius:10px; max-width:900px; margin:20px auto; }
        h2 { color:#ffc107; }
        .item { background:#34495e; margin:8px; padding:12px; border-radius:5px; display:flex; justify-content:space-between; align-items:center; }
        a { color:#28a745; font-weight:bold; text-decoration:none; }
        .back { color:#ffc107; display:block; margin:20px; }
    </style></head><body>
        <h1>{{ flag }} فروشگاه</h1>
        <p>💰 موجودی: {{ gold }} طلا</p>
        <div class="cat"><h2>🏭 تولیدی</h2>
        {% for n, i in items.items() if i.type == 'production' %}
            <div class="item"><span>{{ n }} | {{ i.price }} دلار{% if i.produce %} | درآمد: {{ i.produce }}{% endif %}</span> <a href="/buy/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <div class="cat"><h2>🏥 عمومی</h2>
        {% for n, i in items.items() if i.type == 'general' %}
            <div class="item"><span>{{ n }} | {{ i.price }} دلار</span> <a href="/buy/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <div class="cat"><h2>🪖 نیروی زمینی</h2>
        {% for n, i in units.items() if i.type == 'ground' %}
            <div class="item"><span>{{ n }} | {{ i.price }} دلار | قدرت: {{ i.power }}</span> <a href="/buy_unit/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <div class="cat"><h2>✈️ نیروی هوایی</h2>
        {% for n, i in units.items() if i.type == 'air' %}
            <div class="item"><span>{{ n }} | {{ i.price }} دلار | قدرت: {{ i.power }}</span> <a href="/buy_unit/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <div class="cat"><h2>🚢 نیروی دریایی</h2>
        {% for n, i in units.items() if i.type == 'navy' %}
            <div class="item"><span>{{ n }} | {{ i.price }} دلار | قدرت: {{ i.power }}</span> <a href="/buy_unit/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <a href="/dashboard/{{ country }}" class="back">بازگشت</a>
    </body></html>
    """
    return render_template_string(html, country=country, flag=f, items=BUILDINGS, units=UNITS, gold=d.get("gold", 0))

@app.route('/buy/<country>/<item>')
def buy(country, item):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country)
    b = BUILDINGS.get(item)
    if not b: return "آیتم نامعتبر"
    price = b.get("price", 0)
    if data["countries"][country]["gold"] < price:
        return f"<h3 style='font-family:Tahoma;text-align:center;padding:50px'>طلا کافی نیست! <a href='/shop/{country}'>بازگشت</a></h3>"
    data["countries"][country]["gold"] -= price
    data["countries"][country]["buildings"].append(item)
    database.save_data(data)
    return redirect(f'/dashboard/{country}')

@app.route('/buy_unit/<country>/<unit_key>')
def buy_unit(country, unit_key):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country)
    u = UNITS.get(unit_key)
    if not u: return "واحد نامعتبر"
    check = can_build_unit(country, unit_key)
    if not check["ok"]:
        return f"<h3 style='font-family:Tahoma;text-align:center;padding:50px'>{check['reason']} <a href='/shop/{country}'>بازگشت</a></h3>"
    price = u.get("price", 0)
    if data["countries"][country]["gold"] < price:
        return f"<h3 style='font-family:Tahoma;text-align:center;padding:50px'>طلا کافی نیست! <a href='/shop/{country}'>بازگشت</a></h3>"
    data["countries"][country]["gold"] -= price
    units = data["countries"][country].get("units", {})
    units[unit_key] = units.get(unit_key, 0) + 1
    data["countries"][country]["units"] = units
    database.save_data(data)
    return redirect(f'/my_army/{country}')

@app.route('/my_army/<country>')
def my_army(country):
    if country not in COUNTRIES: return "کشور نیست"
    ensure_country(country)
    d = data["countries"][country]
    units = d.get("units", {})
    buildings = d.get("buildings", [])
    power = calculate_army_power(country)
    upkeep = calculate_upkeep(country)
    html = """
    <div style="font-family:Tahoma;background:#2c3e50;min-height:100vh;color:white;padding:20px;text-align:center">
        <h1>🪖 ارتش {{ country }}</h1>
        <p>💪 قدرت کل: {{ power }} | ⚙️ هزینه نگهداری: {{ upkeep }} طلا</p>
        <div style="background:rgba(0,0,0,0.4);padding:20px;border-radius:10px;max-width:700px;margin:auto">
            <h2>سربازان و تجهیزات</h2>
            {% if units %}
                {% for u, c in units.items() %}<p>{{ u }}: {{ c }} عدد</p>{% endfor %}
            {% else %}<p>هنوز چیزی نداری!</p>{% endif %}
            <h2>ساختمان‌ها</h2>
            {% if buildings %}
                {% for b in buildings %}<p>🏭 {{ b }}</p>{% endfor %}
            {% else %}<p>هنوز ساختمانی نساختی!</p>{% endif %}
        </div>
        <a href="/dashboard/{{ country }}" style="color:#ffc107;display:block;margin-top:20px">بازگشت</a>
    </div>
    """
    return render_template_string(html, country=country, units=units, buildings=buildings, power=power, upkeep=upkeep)

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
            <h1>{{ flag }} بیانیه جدید برای {{ country }}</h1>
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
    country = request.form.get('country')
    target = request.form.get('target')
    text = request.form.get('text')
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
        <h1>📰 بیانیه‌های رسمی</h1>
        <a href="/">بازگشت</a>
        {% for s in statements|reverse %}
            <div class="statement">
                <div class="header">کشور: {{ s.flag }} {{ s.country }}</div>
                <div class="header">مورد: بیانیه 🗞</div>
                <div class="header">خطاب: {{ s.target }}</div>
                <div class="line"></div>
                <div style="line-height:1.8">{{ s.text }}</div>
                <div class="line"></div>
                <div class="end">تمام.</div>
            </div>
        {% endfor %}
        {% if not statements %}<p>هنوز بیانیه‌ای صادر نشده است.</p>{% endif %}
    </body></html>
    """
    return render_template_string(html, statements=data.get("statements", []))

@app.route('/war/<country>')
def war(country):
    return f"""<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'>
    <h1>⚔️ جنگ {country}</h1>
    <p>قدرت ارتش تو: {calculate_army_power(country)}</p>
    <p>سیستم نبرد به‌زودی فعال می‌شود.</p>
    <a href='/dashboard/{country}' style='color:#ffc107'>بازگشت</a></div>"""

@app.route('/map/<country>')
def map_view(country):
    coord = MAP_COORDINATES.get(country, {"lat": 0, "lng": 0})
    return f"""<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'>
    <h1>🗺️ نقشه {country}</h1>
    <p>موقعیت جغرافیایی: عرض {coord['lat']}، طول {coord['lng']}</p>
    <p>سیستم نقشه گرافیکی به‌زودی اضافه می‌شود.</p>
    <a href='/dashboard/{country}' style='color:#ffc107'>بازگشت</a></div>"""

# ============================================================
# پنل ادمین
# ============================================================
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
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>ادمین</title>
    <style>
        body { font-family:Tahoma; background:#2c3e50; color:white; padding:20px; min-height:100vh; }
        .box { background:rgba(0,0,0,0.6); padding:20px; border-radius:10px; max-width:1000px; margin:auto; }
        table { width:100%; border-collapse:collapse; }
        th, td { padding:8px; border-bottom:1px solid #444; font-size:13px; text-align:center; }
        .btn { padding:5px 8px; border:none; border-radius:5px; color:white; text-decoration:none; font-size:11px; display:inline-block; margin:1px; }
        .btn-danger { background:#dc3545; }
        .btn-warning { background:#ffc107; color:#333; }
        .btn-success { background:#28a745; }
        a { color:#ffc107; }
    </style></head><body>
        <div class="box">
            <h1 style="text-align:center">🛡️ پنل ادمین</h1>
            <table>
                <tr><th>کشور</th><th>طلا</th><th>ارتش</th><th>عملیات</th></tr>
                {% for country, flag in countries.items() %}
                    {% if country in status %}
                    <tr>
                        <td>{{ flag }} {{ country }}</td>
                        <td>{{ status[country].get('gold',0) }}</td>
                        <td>{{ status[country].get('units',{})|length }}</td>
                        <td>
                            <a href="/admin/fine/{{ country }}" class="btn btn-warning">جریمه ۲۵۰k</a>
                            <a href="/admin/gold/{{ country }}" class="btn btn-success">+ ۱۰۰k طلا</a>
                            <a href="/admin/delete/{{ country }}" class="btn btn-danger" onclick="return confirm('حذف {{ country }}؟')">حذف</a>
                        </td>
                    </tr>
                    {% endif %}
                {% endfor %}
            </table>
            <br><div style="text-align:center"><a href="/">بازگشت</a> | <a href="/admin/logout">خروج</a></div>
        </div>
    </body></html>
    """
    return render_template_string(html, countries=COUNTRIES, status=data["countries"])

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
        data["countries"][country]["gold"] = data["countries"][country].get("gold", 0) + 100000
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
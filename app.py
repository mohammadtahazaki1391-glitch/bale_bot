import os
from flask import Flask, render_template_string

app = Flask(__name__)

COUNTRIES = ["ایران", "آمریکا", "روسیه", "انگلستان", "آلمان", "فرانسه"]

# وضعیت اولیه کشورها (بعداً با دیتابیس تغییر می‌کنه)
STATUS = {
    "ایران": {"gold": 1000000, "oil": 500, "army": 1000},
    "آمریکا": {"gold": 2000000, "oil": 800, "army": 2000},
    "روسیه": {"gold": 1500000, "oil": 700, "army": 1500},
    "انگلستان": {"gold": 1200000, "oil": 600, "army": 1200},
    "آلمان": {"gold": 1300000, "oil": 550, "army": 1100},
    "فرانسه": {"gold": 1100000, "oil": 500, "army": 900},
}

ITEMS = {
    "پیاده نظام": {"dollar": 50000, "oil": 5, "elec": 10, "ammo": 20, "damage": 150, "defense": 100, "type": "ground"},
    "تانک": {"dollar": 120000, "oil": 20, "elec": 15, "ammo": 50, "damage": 400, "defense": 600, "type": "ground"},
    "موشک انداز": {"dollar": 180000, "oil": 15, "elec": 30, "ammo": 60, "damage": 700, "defense": 150, "type": "ground"},
    "زره پوش": {"dollar": 90000, "oil": 15, "elec": 10, "ammo": 35, "damage": 250, "defense": 400, "type": "ground"},
    "هلیکوپتر تهاجمی": {"dollar": 150000, "oil": 25, "elec": 20, "ammo": 40, "damage": 350, "defense": 250, "type": "air"},
    "جنگنده": {"dollar": 250000, "oil": 35, "elec": 40, "ammo": 30, "damage": 600, "defense": 400, "type": "air"},
    "بمب افکن": {"dollar": 350000, "oil": 50, "elec": 50, "ammo": 20, "damage": 1000, "defense": 300, "type": "air"},
    "پهپاد": {"dollar": 80000, "oil": 10, "elec": 30, "ammo": 15, "damage": 200, "defense": 80, "type": "air"},
    "قایق تندرو": {"dollar": 70000, "oil": 20, "elec": 10, "ammo": 25, "damage": 200, "defense": 150, "type": "navy"},
    "ناوشکن": {"dollar": 220000, "oil": 40, "elec": 30, "ammo": 55, "damage": 500, "defense": 550, "type": "navy"},
    "زیردریایی": {"dollar": 320000, "oil": 30, "elec": 45, "ammo": 40, "damage": 800, "defense": 350, "type": "navy"},
    "ناو هواپیمابر": {"dollar": 500000, "oil": 80, "elec": 100, "ammo": 25, "damage": 1500, "defense": 900, "type": "navy"},
}

DEFENSES = {
    "سامانه پدافند هوایی": {"dollar": 400000, "defense": 1200},
    "موشک ضد هوایی": {"dollar": 250000, "defense": 800},
    "توپ ضد هوایی": {"dollar": 150000, "defense": 500},
}

# صفحه انتخاب کشور
@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>جنگ جهانی</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
            h1 { color: #333; }
            .box { background: white; border-radius: 10px; padding: 20px; margin: 20px auto; max-width: 600px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            ul { list-style: none; padding: 0; }
            li { margin: 10px; padding: 15px; border-radius: 5px; background: #e0e0e0; }
            a { text-decoration: none; color: #333; font-weight: bold; display: block; }
        </style>
    </head>
    <body>
        <h1>به جنگ جهانی خوش آمدید!</h1>
        <h2>یک کشور انتخاب کنید:</h2>
        <div class="box">
            <ul>
                {% for country in countries %}
                    <li><a href="/dashboard/{{ country }}">{{ country }}</a></li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, countries=COUNTRIES)

# منوی اصلی (پنجره چهارتایی)
@app.route('/dashboard/<country>')
def dashboard(country):
    html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>منوی اصلی {{ country }}</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
            h1 { color: #333; }
            .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; max-width: 600px; margin: 20px auto; }.card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: 0.3s; cursor: pointer; text-decoration: none; color: #333; font-weight: bold; font-size: 18px; }
            .card:hover { background: #f0f0f0; }
            .back { display: block; margin-top: 20px; color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>منوی فرماندهی {{ country }}</h1>
        <div class="grid">
            <a href="/status/{{ country }}" class="card">📊 وضعیت کشور</a>
            <a href="/shop/{{ country }}" class="card">🛒 خرید تجهیزات</a>
            <a href="/defense/{{ country }}" class="card">🛡️ پدافند</a>
            <a href="/war/{{ country }}" class="card">⚔️ جنگ و درگیری</a>
        </div>
        <a href="/" class="back">بازگشت به انتخاب کشور</a>
    </body>
    </html>
    """
    return render_template_string(html, country=country)

# وضعیت کشور
@app.route('/status/<country>')
def status(country):
    data = STATUS.get(country, {})
    html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>وضعیت {{ country }}</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
            .box { background: white; border-radius: 10px; padding: 30px; max-width: 400px; margin: 20px auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .back { display: block; margin-top: 20px; color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>وضعیت {{ country }}</h1>
            <p>💰 طلا: {{ data.gold }}</p>
            <p>🛢️ نفت: {{ data.oil }}</p>
            <p>🪖 ارتش: {{ data.army }}</p>
        </div>
        <a href="/dashboard/{{ country }}" class="back">بازگشت به منو</a>
    </body>
    </html>
    """
    return render_template_string(html, country=country, data=data)

# فروشگاه
@app.route('/shop/<country>')
def shop(country):
    html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>فروشگاه {{ country }}</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
            .cat-box { background: white; border-radius: 10px; padding: 20px; margin: 20px auto; max-width: 700px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            h2 { color: #0056b3; }
            ul { list-style: none; padding: 0; }
            li { background: #e0e0e0; margin: 10px; padding: 15px; border-radius: 5px; }
            a { text-decoration: none; color: #333; font-weight: bold; display: block; }
            .back { display: block; margin-top: 20px; color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>فروشگاه {{ country }}</h1>
        <div class="cat-box">
            <h2>نیروی زمینی</h2>
            <ul>{% for name, item in items.items() if item.type == 'ground' %}<li><a href="#">{{ name }}</a></li>{% endfor %}</ul>
        </div>
        <div class="cat-box">
            <h2>نیروی هوایی</h2>
            <ul>{% for name, item in items.items() if item.type == 'air' %}<li><a href="#">{{ name }}</a></li>{% endfor %}</ul>
        </div>
        <div class="cat-box">
            <h2>نیروی دریایی</h2>
            <ul>{% for name, item in items.items() if item.type == 'navy' %}<li><a href="#">{{ name }}</a></li>{% endfor %}</ul>
        </div>
        <a href="/dashboard/{{ country }}" class="back">بازگشت به منو</a>
    </body>
    </html>
    """
    return render_template_string(html, country=country, items=ITEMS)

# پدافند
@app.route('/defense/<country>')
def defense(country):html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>پدافند {{ country }}</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
            .box { background: white; border-radius: 10px; padding: 20px; max-width: 500px; margin: 20px auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            ul { list-style: none; padding: 0; }
            li { background: #e0e0e0; margin: 10px; padding: 15px; border-radius: 5px; }
            a { text-decoration: none; color: #333; font-weight: bold; display: block; }
            .back { display: block; margin-top: 20px; color: #007bff; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>پدافند {{ country }}</h1>
        <div class="box">
            <ul>
                {% for name, defense in defenses.items() %}
                    <li>{{ name }} (دفاع: {{ defense.defense }})</li>
                {% endfor %}
            </ul>
        </div>
        <a href="/dashboard/{{ country }}" class="back">بازگشت به منو</a>
    </body>
    </html>
    """
    return render_template_string(html, country=country, defenses=DEFENSES)

# صفحه جنگ (فعلاً ساده)
@app.route('/war/<country>')
def war(country):
    return f"<h1>جنگ {country}</h1><p>برای پیاده‌سازی جنگ آنلاین و محاصره دریایی، به پایگاه داده نیاز داریم. این بخش بعداً تکمیل می‌شود.</p><a href='/dashboard/{country}'>بازگشت</a>"

port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port)

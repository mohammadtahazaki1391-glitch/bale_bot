import os
from flask import Flask, render_template_string

app = Flask(__name__)

COUNTRIES = ["ایران", "آمریکا", "روسیه", "انگلستان", "آلمان", "فرانسه"]

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
            h2 { color: #0056b3; }
            .cat-box { background: white; border-radius: 10px; padding: 20px; margin: 20px auto; max-width: 700px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            ul { list-style: none; padding: 0; }
            li { background: #e0e0e0; margin: 10px; padding: 15px; border-radius: 5px; }
            a { text-decoration: none; color: #333; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>به جنگ جهانی خوش آمدید!</h1>
        <div class="cat-box">
            <h2>کشورها</h2>
            <ul>
                {% for country in countries %}
                    <li>{{ country }}</li>
                {% endfor %}
            </ul>
        </div>
        <div class="cat-box">
            <h2>نیروی زمینی</h2>
            <ul>
                {% for name, item in items.items() if item.type == 'ground' %}
                    <li><a href="/buy/{{ name }}">{{ name }}</a></li>
                {% endfor %}
            </ul>
        </div>
        <div class="cat-box">
            <h2>نیروی هوایی</h2>
            <ul>
                {% for name, item in items.items() if item.type == 'air' %}
                    <li><a href="/buy/{{ name }}">{{ name }}</a></li>
                {% endfor %}
            </ul>
        </div>
        <div class="cat-box">
            <h2>نیروی دریایی</h2>
            <ul>
                {% for name, item in items.items() if item.type == 'navy' %}
                    <li><a href="/buy/{{ name }}">{{ name }}</a></li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, countries=COUNTRIES, items=ITEMS)

@app.route('/buy/<item_name>')
def buy_item(item_name):
    item = ITEMS.get(item_name)
    if not item:
        return "آیتم پیدا نشد!", 404
    
    html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl"><head>
        <meta charset="UTF-8">
        <title>خرید {{ item_name }}</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
            .box { background: white; border-radius: 10px; padding: 30px; margin: 20px auto; max-width: 400px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            p { font-size: 18px; }
            a { text-decoration: none; color: white; background: #dc3545; padding: 10px 20px; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>{{ item_name }}</h1>
            <p>قیمت: {{ item.dollar }} دلار</p>
            <p>نفت: {{ item.oil }} | برق: {{ item.elec }} | مهمات: {{ item.ammo }}</p>
            <p>خسارت: {{ item.damage }} | دفاع: {{ item.defense }}</p>
            <p>نوع نیرو: {{ item.type }}</p>
            <a href="/">بازگشت به فروشگاه</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, item=item, item_name=item_name)

port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port)

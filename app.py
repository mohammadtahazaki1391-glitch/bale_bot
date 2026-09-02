import os
from flask import Flask, render_template_string

app = Flask(__name__)

# داده‌های بازی (همان‌هایی که داشتی)
COUNTRIES = ["ایران", "آمریکا", "روسیه", "انگلستان", "آلمان", "فرانسه"]
ITEMS = {
    "مک‌بوک": {"dollar": 160000, "oil": 10, "elec": 50, "ammo": 30, "damage": 200, "defense": 600, "type": "air"},
    "آیفون": {"dollar": 150000, "oil": 10, "elec": 45, "ammo": 25, "damage": 190, "defense": 500, "type": "air"},
}

# صفحه اصلی سایت
@app.route('/')
def home():
    # یک HTML ساده که لیست کشورها و آیتم‌ها را نشان می‌دهد
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
            li { background: #e0e0e0; margin: 10px; padding: 10px; border-radius: 5px; }
            .btn { background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>به جنگ جهانی خوش آمدید!</h1>
        <div class="box">
            <h2>کشورها</h2>
            <ul>
                {% for country in countries %}
                    <li>{{ country }}</li>
                {% endfor %}
            </ul>
        </div>
        <div class="box">
            <h2>تجهیزات</h2>
            <ul>
                {% for name, item in items.items() %}
                    <li>
                        <strong>{{ name }}</strong><br>
                        قیمت: {{ item.dollar }} دلار | خسارت: {{ item.damage }} | دفاع: {{ item.defense }}
                    </li>
                {% endfor %}
            </ul>
            <button class="btn">شروع بازی</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, countries=COUNTRIES, items=ITEMS)

# برای اینکه رندر سایت را خاموش نکند، پورت را می‌گیریم و اجرا می‌کنیم
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

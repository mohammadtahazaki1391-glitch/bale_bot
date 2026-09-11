import os
from flask import Flask, render_template_string, request, redirect, make_response, jsonify

app = Flask(__name__)

# ذخیره موقت پیام‌های چت (در مرحله بعد می‌تونیم به دیتابیس وصل کنیم)
chat_messages = []

COUNTRIES = ["ایران", "آمریکا", "روسیه", "انگلستان", "آلمان", "فرانسه"]

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
    "هلیکوپتر تهاجمی": {"dollar": 150000, "oil": 25, "elec": 20, "ammo": 40, "damage": 350, "defense": 250, "type": "air"},
    "جنگنده": {"dollar": 250000, "oil": 35, "elec": 40, "ammo": 30, "damage": 600, "defense": 400, "type": "air"},
    "قایق تندرو": {"dollar": 70000, "oil": 20, "elec": 10, "ammo": 25, "damage": 200, "defense": 150, "type": "navy"},
    "ناوشکن": {"dollar": 220000, "oil": 40, "elec": 30, "ammo": 55, "damage": 500, "defense": 550, "type": "navy"},
}

@app.route('/')
def home():
    selected = request.cookies.get('country')
    if selected in COUNTRIES:
        return redirect(f'/dashboard/{selected}')
    
    # ⬇️ اینجا آدرس Raw عکس رو جایگزین کن (اگر خواستی عکس رو اضافه کنی)
    IMAGE_URL = "" 
    
    html = """
    <div style="font-family:Tahoma;text-align:center;padding:50px">
        {% if image_url %}<img src="{{ image_url }}" style="max-width:100%; height:auto; border-radius:10px; margin-bottom:20px;">{% endif %}
        <h1>جنگ جهانی</h1>
        <h3>یک کشور انتخاب کنید</h3>
        <ul style="list-style:none;padding:0">
        {% for country in countries %}
            <li style="margin:10px"><a href="/set_country/{{ country }}" style="background:#e0e0e0;padding:15px;display:block;border-radius:5px;text-decoration:none;color:#333">{{ country }}</a></li>
        {% endfor %}
        </ul>
    </div>
    """
    return render_template_string(html, countries=COUNTRIES, image_url=IMAGE_URL)

@app.route('/set_country/<country>')
def set_country(country):
    resp = make_response(redirect(f'/dashboard/{country}'))
    resp.set_cookie('country', country)
    return resp

@app.route('/dashboard/<country>')
def dashboard(country):
    html = """
    <div style="font-family:Tahoma;text-align:center;padding:20px">
        <h1>منوی فرماندهی {{ country }}</h1>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:600px;margin:auto">
            <a href="/status/{{ country }}" style="background:white;padding:30px;border-radius:10px;text-decoration:none;color:#333;font-size:20px">📊 وضعیت</a>
            <a href="/shop/{{ country }}" style="background:white;padding:30px;border-radius:10px;text-decoration:none;color:#333;font-size:20px">🛒 خرید</a>
            <a href="/defense/{{ country }}" style="background:white;padding:30px;border-radius:10px;text-decoration:none;color:#333;font-size:20px">🛡️ پدافند</a>
            <a href="/chat" style="background:#007bff;color:white;padding:30px;border-radius:10px;text-decoration:none;font-size:20px">💬 چت</a>
        </div>
        <a href="/reset" style="display:block;margin-top:30px;color:red">تغییر کشور</a>
    </div>
    """
    return render_template_string(html, country=country)

# --- API برای چت ---
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    country = request.cookies.get('country', 'ناشناس')
    msg = data.get('message', '')
    if msg:
        chat_messages.append({"sender": country, "text": msg})
    return jsonify({"status": "ok"})

@app.route('/api/get_messages')
def get_messages():
    return jsonify(chat_messages)

# --- صفحه چت ---
@app.route('/chat')
def chat():
    html = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>چت جهانی</title>
        <style>
            body { margin: 0; padding: 0; background-color: #2c3e50; font-family: Tahoma; }
            .chat-container {
                position: absolute; bottom: 20px; left: 20px;
                width: 350px; height: 250px;
                background-color: rgba(0, 0, 0, 0.8);
                border: 1px solid #444; color: white;
                display: flex; flex-direction: column; z-index: 1000; border-radius: 8px;
            }
            .chat-history { flex-grow: 1; overflow-y: auto; padding: 10px; font-size: 13px; }
            .chat-history p { margin: 5px 0; }
            .chat-input-area { padding: 5px; display: flex; border-top: 1px solid #444; }
            .chat-input-area input { flex-grow: 1; padding: 8px; border: none; background: #333; color: white; border-radius: 4px; }
            .chat-input-area button { padding: 8px 15px; margin-right: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div id="chat-box" class="chat-container">
            <div id="chat-history" class="chat-history"></div>
            <div class="chat-input-area">
                <input type="text" id="chat-input" placeholder="پیام...">
                <button onclick="sendMessage()">ارسال</button>
            </div>
        </div>

        <script>
            const chatHistory = document.getElementById('chat-history');
            const chatInput = document.getElementById('chat-input');

            function sendMessage() {
                const text = chatInput.value;
                if (text.trim() === '') return;
                fetch('/api/send_message', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                }).then(() => { chatInput.value = ''; loadMessages(); });
            }

            function loadMessages() {
                fetch('/api/get_messages')
                .then(res => res.json())
                .then(data => {
                    chatHistory.innerHTML = '';
                    data.forEach(msg => {
                        chatHistory.innerHTML += `<p><b>${msg.sender}:</b> ${msg.text}</p>`;
                    });
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                });
            }

            // هر ۲ ثانیه یکبار پیام‌های جدید رو چک کن
            setInterval(loadMessages, 2000);
            loadMessages();

            // با زدن دکمه Enter هم پیام ارسال بشه
            chatInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/status/<country>')
def status(country):
    data = STATUS.get(country, {})
    return f"<div style='font-family:Tahoma;text-align:center;padding:50px'><h1>وضعیت {country}</h1><p>💰 طلا: {data['gold']}</p><p>🛢 نفت: {data['oil']}</p><p>🪖 ارتش: {data['army']}</p><br><a href='/dashboard/{country}'>بازگشت به منو</a></div>"

@app.route('/shop/<country>')
def shop(country):
    html = """
    <div style="font-family:Tahoma;text-align:center;padding:20px">
        <h1>فروشگاه {{ country }}</h1>
        <div style="max-width:600px;margin:auto">
        {% for name, item in items.items() %}
            <div style="background:white;margin:10px;padding:15px;border-radius:5px">
                <h3>{{ name }}</h3>
                <p>قیمت: {{ item.dollar }} دلار | خسارت: {{ item.damage }} | دفاع: {{ item.defense }}</p>
                <a href="/buy/{{ country }}/{{ name }}">خرید</a>
            </div>
        {% endfor %}
        </div>
        <a href="/dashboard/{{ country }}">بازگشت</a>
    </div>
    """
    return render_template_string(html, country=country, items=ITEMS)

@app.route('/buy/<country>/<item>')
def buy(country, item):
    if country not in STATUS: return "کشور نامعتبر"
    item_data = ITEMS.get(item)
    if not item_data: return "آیتم نامعتبر"
    
    price = item_data['dollar']
    oil_needed = item_data['oil']
    
    if STATUS[country]['gold'] < price or STATUS[country]['oil'] < oil_needed:
        return f"<h3>منابع کافی نیست! طلا و نفت بیشتری لازم داری.</h3><a href='/shop/{country}'>بازگشت</a>"
    
    STATUS[country]['gold'] -= price
    STATUS[country]['oil'] -= oil_needed
    STATUS[country]['army'] += 10
    
    return f"<div style='font-family:Tahoma;text-align:center;padding:50px'><h2>✅ خرید موفق!</h2><p>شما {item} را خریدید.</p><p>موجودی طلا: {STATUS[country]['gold']}</p><a href='/dashboard/{country}'>بازگشت به منو</a></div>"

@app.route('/defense/<country>')
def defense(country):
    return f"<div style='font-family:Tahoma;text-align:center;padding:50px'><h1>پدافند {country}</h1><p>سیستم پدافندی فعال است.</p><a href='/dashboard/{country}'>بازگشت</a></div>"

@app.route('/war/<country>')
def war(country):
    return f"<div style='font-family:Tahoma;text-align:center;padding:50px'><h1>جنگ {country}</h1><p>برای جنگ آنلاین بین چند کشور، نیاز به دیتابیس داریم که در مرحله بعد اضافه می‌شود.</p><a href='/dashboard/{country}'>بازگشت</a></div>"

@app.route('/reset')
def reset():
    resp = make_response(redirect('/'))
    resp.delete_cookie('country')
    return resp

port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port)
import os
from flask import Flask, render_template_string, request, redirect, make_response, jsonify, session

app = Flask(__name__)
app.secret_key = "secret_key_123"
ADMIN_PASSWORD = "admin123"

chat_messages = []
statements = []

# کشورها با پرچم
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

# وضعیت پیش‌فرض همه کشورها
STATUS = {}
for c in COUNTRIES:
    STATUS[c] = {"gold": 1000000, "oil": 500, "army": 1000, "uranium": 10, "weapons": 500, "elec": 500}

# تجهیزات
ITEMS = {
    # --- تولیدی ---
    "معدن اورانیوم": {"price": 100000, "currency": "dollar", "type": "production", "income": "2 اورانیوم"},
    "پالایشگاه نفت": {"price": 75000, "currency": "dollar", "type": "production", "income": "50 نفت"},
    "کارخونه اسلحه": {"price": 50000, "currency": "dollar", "type": "production", "income": "50 اسلحه"},
    "معدن طلا": {"price": 150000, "currency": "dollar", "type": "production", "income": "2 طلا"},
    "شهر": {"price": 250000, "currency": "dollar", "type": "production", "income": "100000 دلار"},

    # --- عمومی ---
    "بیمارستان": {"price": 10000, "currency": "dollar", "type": "general"},
    "پایگاه پلیس": {"price": 10000, "currency": "dollar", "type": "general"},
    "سد": {"price": 15000, "currency": "dollar", "type": "general"},

    # --- نظامی: زمینی ---
    "تانک ابرامز": {"price": 500000, "currency": "dollar", "type": "ground", "damage": 800, "defense": 600},
    "تانک تی14 ارماتا": {"price": 550000, "currency": "dollar", "type": "ground", "damage": 850, "defense": 700},
    "تانک لئوپارد": {"price": 480000, "currency": "dollar", "type": "ground", "damage": 780, "defense": 620},
    "تانک چلنجر": {"price": 470000, "currency": "dollar", "type": "ground", "damage": 760, "defense": 650},
    "تانک تایپ99": {"price": 460000, "currency": "dollar", "type": "ground", "damage": 740, "defense": 630},
    "تانک پوکجان": {"price": 300000, "currency": "dollar", "type": "ground", "damage": 500, "defense": 450},
    "تانک کرار": {"price": 280000, "currency": "dollar", "type": "ground", "damage": 480, "defense": 420},
    "سرباز عادی": {"price": 5000, "currency": "dollar", "type": "ground", "damage": 50, "defense": 30},
    "سرباز تکاور": {"price": 12000, "currency": "dollar", "type": "ground", "damage": 120, "defense": 80},
    "سرباز ارپیجی": {"price": 15000, "currency": "dollar", "type": "ground", "damage": 200, "defense": 60},
    "سرباز اسنایپر": {"price": 18000, "currency": "dollar", "type": "ground", "damage": 250, "defense": 40},
    "کماندو": {"price": 25000, "currency": "dollar", "type": "ground", "damage": 300, "defense": 150},
    "لانچر LGM-HOPML": {"price": 400000, "currency": "dollar", "type": "ground", "damage": 900, "defense": 100},
    "لانچر SERMET-ROY": {"price": 380000, "currency": "dollar", "type": "ground", "damage": 850, "defense": 120},
    "لانچر HQ-ETY21": {"price": 420000, "currency": "dollar", "type": "ground", "damage": 950, "defense": 90},
    "لانچر IL-GONDEY": {"price": 350000, "currency": "dollar", "type": "ground", "damage": 800, "defense": 110},
    "لانچر CHL-V56": {"price": 360000, "currency": "dollar", "type": "ground", "damage": 820, "defense": 100},

    # --- نظامی: هوایی ---
    "بمب افکن بلک برد": {"price": 2000000, "currency": "dollar", "type": "air", "damage": 3000, "defense": 500},
    "بمب افکن بی دو": {"price": 1800000, "currency": "dollar", "type": "air", "damage": 2800, "defense": 450},
    "بمب افکن اچ20": {"price": 1500000, "currency": "dollar", "type": "air", "damage": 2500, "defense": 400},
    "بمب افکن دورینه": {"price": 1200000, "currency": "dollar", "type": "air", "damage": 2200, "defense": 350},
    "بمب افکن تی یو 160": {"price": 1900000, "currency": "dollar", "type": "air", "damage": 2900, "defense": 480},
    "جنگنده اف 35": {"price": 1000000, "currency": "dollar", "type": "air", "damage": 1200, "defense": 800},
    "جنگنده سوخو57": {"price": 950000, "currency": "dollar", "type": "air", "damage": 1150, "defense": 780},
    "جنگنده تمپست": {"price": 900000, "currency": "dollar", "type": "air", "damage": 1100, "defense": 750},
    "جنگنده MIG-29": {"price": 700000, "currency": "dollar", "type": "air", "damage": 900, "defense": 600},
    "پهباد SHAHED-238": {"price": 200000, "currency": "dollar", "type": "air", "damage": 400, "defense": 150},

    # --- نظامی: دریایی ---
    "ناو هواپیمابر جرالد فورد": {"price": 5000000, "currency": "dollar", "type": "navy", "damage": 4000, "defense": 3000},
    "ناو هواپیمابر فوجیان": {"price": 4500000, "currency": "dollar", "type": "navy", "damage": 3800, "defense": 2800},
    "ناو هواپیمابر ملکه الیزابت": {"price": 4200000, "currency": "dollar", "type": "navy", "damage": 3600, "defense": 2700},
    "ناو هواپیمابر کوزنتسوف": {"price": 3500000, "currency": "dollar", "type": "navy", "damage": 3200, "defense": 2400},
    "ناو هواپیمابر گراف": {"price": 3800000, "currency": "dollar", "type": "navy", "damage": 3400, "defense": 2500},
    "ناوشکن آرلی برک": {"price": 1500000, "currency": "dollar", "type": "navy", "damage": 1500, "defense": 1200},
    "ناوشکن آدمیرال گورشکوف": {"price": 1300000, "currency": "dollar", "type": "navy", "damage": 1300, "defense": 1100},
}

@app.route('/')
def home():
    selected = request.cookies.get('country')
    if selected in COUNTRIES:
        return redirect(f'/dashboard/{selected}')
    IMAGE_URL = ""
    html = """
    <div style="font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white">
        {% if image_url %}<img src="{{ image_url }}" style="max-width:100%;border-radius:10px;margin-bottom:20px;">{% endif %}
        <h1>🌍 جنگ جهانی</h1>
        <h3>یک کشور انتخاب کنید</h3>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px;max-width:1100px;margin:auto">
        {% for country, flag in countries.items() %}
            <a href="/set_country/{{ country }}" style="background:#34495e;padding:8px;border-radius:5px;text-decoration:none;color:white;font-size:13px">{{ flag }} {{ country }}</a>
        {% endfor %}
        </div>
    </div>
    """
    return render_template_string(html, countries=COUNTRIES, image_url=IMAGE_URL)

@app.route('/set_country/<country>')
def set_country(country):
    if country not in COUNTRIES:
        return "این کشور حذف شده است!", 404
    resp = make_response(redirect(f'/dashboard/{country}'))
    resp.set_cookie('country', country)
    return resp

@app.route('/dashboard/<country>')
def dashboard(country):
    if country not in COUNTRIES:
        return "این کشور حذف شده است!", 404
    flag = COUNTRIES[country]
    html = """
    <div style="font-family:Tahoma;text-align:center;padding:20px;background:#2c3e50;min-height:100vh;color:white">
        <h1>{{ flag }} منوی فرماندهی {{ country }}</h1>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;max-width:700px;margin:auto">
            <a href="/status/{{ country }}" style="background:#34495e;padding:25px;border-radius:10px;text-decoration:none;color:white;font-size:18px">📊 وضعیت</a>
            <a href="/shop/{{ country }}" style="background:#34495e;padding:25px;border-radius:10px;text-decoration:none;color:white;font-size:18px">🛒 فروشگاه</a>
            <a href="/defense/{{ country }}" style="background:#34495e;padding:25px;border-radius:10px;text-decoration:none;color:white;font-size:18px">🛡️ پدافند</a>
            <a href="/chat" style="background:#007bff;color:white;padding:25px;border-radius:10px;text-decoration:none;font-size:18px">💬 چت</a>
            <a href="/create_statement/{{ country }}" style="background:#ffc107;color:#333;padding:25px;border-radius:10px;text-decoration:none;font-size:18px">📜 بیانیه جدید</a>
            <a href="/statements" style="background:#28a745;color:white;padding:25px;border-radius:10px;text-decoration:none;font-size:18px">📰 بیانیه‌ها</a>
        </div>
        <a href="/reset" style="display:block;margin-top:20px;color:#e74c3c">تغییر کشور</a>
        <a href="/admin" style="display:block;margin-top:10px;color:#95a5a6;font-size:12px">ورود ادمین</a>
    </div>
    """
    return render_template_string(html, country=country, flag=flag)

# چت
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    country = request.cookies.get('country', 'ناشناس')
    msg = data.get('message', '')
    flag = COUNTRIES.get(country, "🏳")
    if msg:
        chat_messages.append({"sender": f"{flag} {country}", "text": msg})
    return jsonify({"status": "ok"})

@app.route('/api/get_messages')
def get_messages():
    return jsonify(chat_messages)

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
            setInterval(load, 2000); load();
            ci.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });
        </script>
    </body></html>
    """
    return render_template_string(html, country=country)

# بیانیه
@app.route('/create_statement/<country>')
def create_statement(country):
    if country not in COUNTRIES:
        return "کشور نامعتبر", 404
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
                    {% for c, f in countries.items() %}
                        {% if c != country %}<option value="{{ f }} {{ c }}">{{ f }} {{ c }}</option>{% endif %}
                    {% endfor %}
                </select>
                <textarea name="text" placeholder="متن بیانیه خود را اینجا بنویسید..."></textarea>
                <button type="submit">ارسال بیانیه</button>
            </form>
            <a href="/dashboard/{{ country }}">بازگشت</a>
        </div>
    </body></html>
    """
    return render_template_string(html, country=country, flag=flag, countries=COUNTRIES)

@app.route('/save_statement', methods=['POST'])
def save_statement():
    country = request.form.get('country')
    target = request.form.get('target')
    text = request.form.get('text')
    flag = COUNTRIES.get(country, "🏳")
    if country and text:
        statements.append({"country": country, "flag": flag, "target": target, "text": text})
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
        <a href="/">بازگشت به خانه</a>
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
    return render_template_string(html, statements=statements)

# ادمین
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
        else:
            return "رمز اشتباه است! <a href='/admin'>تلاش مجدد</a>"
    if not session.get('admin'):
        return """<div style="font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white">
            <h1>ورود ادمین</h1>
            <form method="POST">
                <input type="password" name="password" placeholder="رمز عبور" style="padding:10px;font-size:16px">
                <button type="submit" style="padding:10px 20px;background:#007bff;color:white;border:none;border-radius:5px">ورود</button>
            </form>
            <a href="/" style="color:#ffc107">بازگشت</a></div>"""
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>پنل ادمین</title>
    <style>
        body { font-family:Tahoma; background:#2c3e50; color:white; text-align:center; padding:20px; min-height:100vh; }
        .box { background:rgba(0,0,0,0.6); padding:20px; border-radius:10px; max-width:800px; margin:20px auto; }
        table { width:100%; border-collapse:collapse; margin-top:20px; }
        th, td { padding:8px; border-bottom:1px solid #444; font-size:14px; }
        .btn { padding:6px 10px; border:none; border-radius:5px; cursor:pointer; text-decoration:none; color:white; display:inline-block; margin:2px; font-size:12px; }
        .btn-danger { background:#dc3545; }
        .btn-warning { background:#ffc107; color:#333; }
        a { color:#ffc107; }
    </style></head><body>
        <div class="box">
            <h1>🛡️ پنل ادمین</h1>
            <table>
                <tr><th>کشور</th><th>طلا</th><th>عملیات</th></tr>
                {% for country, flag in countries.items() %}
                <tr>
                    <td>{{ flag }} {{ country }}</td>
                    <td>{{ status[country]['gold'] }}</td>
                    <td>
                        <a href="/admin/fine/{{ country }}" class="btn btn-warning">جریمه ۲۵۰,۰۰۰</a>
                        <a href="/admin/delete/{{ country }}" class="btn btn-danger" onclick="return confirm('حذف {{ country }}؟')">حذف</a>
                    </td>
                </tr>
                {% endfor %}
            </table>
            <br><a href="/">بازگشت</a> | <a href="/admin/logout">خروج</a>
        </div>
    </body></html>
    """
    return render_template_string(html, countries=COUNTRIES, status=STATUS)

@app.route('/admin/fine/<country>')
def admin_fine(country):
    if not session.get('admin'): return redirect('/admin')
    if country in STATUS: STATUS[country]['gold'] -= 250000
    return redirect('/admin')

@app.route('/admin/delete/<country>')
def admin_delete(country):
    if not session.get('admin'): return redirect('/admin')
    if country in COUNTRIES: del COUNTRIES[country]
    if country in STATUS: del STATUS[country]
    return redirect('/admin')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/')

# وضعیت
@app.route('/status/<country>')
def status(country):
    if country not in COUNTRIES: return "کشور حذف شده", 404
    d = STATUS.get(country, {})
    f = COUNTRIES[country]
    return f"""<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'>
    <h1>{f} وضعیت {country}</h1>
    <p>💰 طلا: {d.get('gold',0)}</p>
    <p>🛢 نفت: {d.get('oil',0)}</p>
    <p>☢️ اورانیوم: {d.get('uranium',0)}</p>
    <p>🔫 اسلحه: {d.get('weapons',0)}</p>
    <p>⚡ برق: {d.get('elec',0)}</p>
    <p>🪖 ارتش: {d.get('army',0)}</p>
    <br><a href='/dashboard/{country}' style='color:#ffc107'>بازگشت</a></div>"""

# فروشگاه
@app.route('/shop/<country>')
def shop(country):
    if country not in COUNTRIES: return "کشور حذف شده", 404
    f = COUNTRIES[country]
    html = """
    <!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>فروشگاه</title>
    <style>
        body { font-family:Tahoma; background:#2c3e50; color:white; text-align:center; padding:20px; min-height:100vh; }
        .cat { background:rgba(0,0,0,0.6); padding:20px; border-radius:10px; max-width:800px; margin:20px auto; }
        h2 { color:#ffc107; }
        .item { background:#34495e; margin:8px; padding:12px; border-radius:5px; text-align:right; }
        a { color:#28a745; font-weight:bold; }
        .back { color:#ffc107; display:block; margin:20px; }
    </style></head><body>
        <h1>{{ flag }} فروشگاه {{ country }}</h1>
        <div class="cat"><h2>🏭 تولیدی</h2>
        {% for n, i in items.items() if i.type == 'production' %}
            <div class="item">{{ n }} | قیمت: {{ i.price }} دلار | درآمد: {{ i.income }} <a href="/buy/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <div class="cat"><h2>🏥 عمومی</h2>
        {% for n, i in items.items() if i.type == 'general' %}
            <div class="item">{{ n }} | قیمت: {{ i.price }} دلار <a href="/buy/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <div class="cat"><h2>🪖 نیروی زمینی</h2>
        {% for n, i in items.items() if i.type == 'ground' %}
            <div class="item">{{ n }} | {{ i.price }} دلار | خسارت: {{ i.damage }} | دفاع: {{ i.defense }} <a href="/buy/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <div class="cat"><h2>✈️ نیروی هوایی</h2>
        {% for n, i in items.items() if i.type == 'air' %}
            <div class="item">{{ n }} | {{ i.price }} دلار | خسارت: {{ i.damage }} | دفاع: {{ i.defense }} <a href="/buy/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <div class="cat"><h2>🚢 نیروی دریایی</h2>
        {% for n, i in items.items() if i.type == 'navy' %}
            <div class="item">{{ n }} | {{ i.price }} دلار | خسارت: {{ i.damage }} | دفاع: {{ i.defense }} <a href="/buy/{{ country }}/{{ n }}">[خرید]</a></div>
        {% endfor %}</div>
        <a href="/dashboard/{{ country }}" class="back">بازگشت به منو</a>
    </body></html>
    """
    return render_template_string(html, country=country, flag=f, items=ITEMS)

@app.route('/buy/<country>/<item>')
def buy(country, item):
    if country not in STATUS: return "کشور نامعتبر"
    item_data = ITEMS.get(item)
    if not item_data: return "آیتم نامعتبر"
    price = item_data.get('price', 0)
    if STATUS[country]['gold'] < price:
        return f"<h3>طلا کافی نیست!</h3><a href='/shop/{country}'>بازگشت</a>"
    STATUS[country]['gold'] -= price
    return f"<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'><h2>✅ خرید موفق!</h2><p>{item} خریداری شد.</p><p>موجودی: {STATUS[country]['gold']}</p><a href='/dashboard/{country}' style='color:#ffc107'>بازگشت</a></div>"

@app.route('/defense/<country>')
def defense(country):
    return f"<div style='font-family:Tahoma;text-align:center;padding:50px;background:#2c3e50;min-height:100vh;color:white'><h1>🛡️ پدافند {COUNTRIES.get(country,'')} {country}</h1><p>فعال</p><a href='/dashboard/{country}' style='color:#ffc107'>بازگشت</a></div>"

@app.route('/reset')
def reset():
    resp = make_response(redirect('/'))
    resp.delete_cookie('country')
    return resp

port = int(os.environ.get('PORT', 10000))
app.run(host='0.0.0.0', port=port)
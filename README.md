# 🎬 Saba TV - نظام إدارة IPTV

نظام متكامل لإدارة خدمات IPTV مع لوحة تحكم للمدير والموزعين.

---

## 🌟 الميزات الرئيسية

### 👨‍💼 لوحة تحكم المدير
- ✅ إدارة الموزعين (إضافة، تعديل، حذف)
- ✅ توزيع النقاط على الموزعين
- ✅ عرض إحصائيات شاملة
- ✅ إدارة جميع الأجهزة
- ✅ إدارة روابط M3U
- ✅ سجل المعاملات الكامل

### 🏪 لوحة تحكم الموزع
- ✅ عرض رصيد النقاط
- ✅ إضافة أجهزة جديدة
- ✅ إدارة الأجهزة الخاصة
- ✅ تتبع تواريخ الانتهاء
- ✅ سجل المعاملات الشخصي

### 📱 API للتطبيقات
- ✅ التحقق من MAC Address
- ✅ إرجاع رابط M3U8 للجهاز
- ✅ التحقق من صلاحية الاشتراك
- ✅ دعم روابط M3U مخصصة لكل جهاز

### 🎨 الواجهة
- ✅ تصميم عصري ومتجاوب
- ✅ دعم كامل للغة العربية (RTL)
- ✅ ألوان جذابة ومريحة للعين
- ✅ تجربة مستخدم سلسة

---

## 🚀 التقنيات المستخدمة

### Backend
- **Flask** - إطار عمل Python
- **SQLAlchemy** - ORM لقاعدة البيانات
- **Flask-CORS** - دعم CORS
- **JWT** - المصادقة الآمنة

### Frontend
- **React** - مكتبة JavaScript
- **Vite** - أداة البناء
- **TailwindCSS** - تصميم الواجهة
- **Axios** - طلبات HTTP

### Database
- **SQLite** - للتطوير المحلي
- **PostgreSQL** - للإنتاج (Railway/Render)

---

## 📦 التثبيت المحلي

### المتطلبات
- Python 3.11+
- Node.js 22+
- npm أو yarn

### الخطوات

#### 1. استنساخ المشروع
```bash
git clone https://github.com/yaseenyaseen123/saba-tv.git
cd saba-tv
```

#### 2. إعداد Backend
```bash
cd src
pip install -r ../requirements.txt
python main.py
```

#### 3. إعداد Frontend (في نافذة أخرى)
```bash
cd saba-tv-dashboard
npm install
npm run dev
```

#### 4. الوصول إلى التطبيق
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

---

## 🔐 بيانات الدخول الافتراضية

### المدير
- **اسم المستخدم:** `admin`
- **كلمة المرور:** `admin123`

### موزع تجريبي
- **اسم المستخدم:** `test123`
- **كلمة المرور:** `test123`
- **النقاط:** 100

---

## 🌐 النشر على الإنترنت

### خيار 1: Railway (موصى به) 💰 $5/شهر

#### المميزات
- ✅ قاعدة بيانات PostgreSQL مجانية
- ✅ SSL مجاني
- ✅ لا يتوقف أبداً
- ✅ أداء ممتاز
- ✅ سهل الإعداد

#### الخطوات
1. افتح https://railway.app
2. سجل دخول بـ GitHub
3. اضغط "New Project"
4. اختر "Deploy from GitHub repo"
5. اختر مستودع `saba-tv`
6. أضف قاعدة بيانات PostgreSQL
7. انتظر حتى ينتهي البناء
8. احصل على الرابط من Settings → Generate Domain

---

### خيار 2: Render (مجاني) 🆓

#### المميزات
- ✅ مجاني تماماً
- ✅ قاعدة بيانات PostgreSQL مجانية
- ✅ SSL مجاني
- ⚠️ يتوقف بعد 15 دقيقة من عدم الاستخدام

#### الخطوات
1. افتح https://render.com
2. سجل دخول بـ GitHub
3. اضغط "New +" → "Web Service"
4. اختر مستودع `saba-tv`
5. املأ البيانات:
   - **Name:** saba-tv
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd src && python main.py`
6. أضف قاعدة بيانات PostgreSQL
7. اربط DATABASE_URL
8. اضغط "Create Web Service"

---

## 📱 API للتطبيقات

### Endpoint: التحقق من الجهاز

**URL:**
```
POST /api/device/verify
```

**Request Body:**
```json
{
  "mac_address": "AA:BB:CC:DD:EE:FF"
}
```

**Response (نشط):**
```json
{
  "status": "active",
  "m3u_url": "http://server.com/playlist.m3u8",
  "m3u_name": "رابط القنوات",
  "expiry_date": "2026-10-07",
  "days_left": 365,
  "customer_name": "محمد أحمد"
}
```

**Response (منتهي):**
```json
{
  "status": "expired",
  "message": "انتهت صلاحية الاشتراك",
  "expiry_date": "2024-01-01"
}
```

**Response (غير موجود):**
```json
{
  "status": "not_found",
  "message": "الجهاز غير مسجل في النظام"
}
```

### مثال Python
```python
import requests

url = "https://your-domain.com/api/device/verify"
data = {"mac_address": "AA:BB:CC:DD:EE:FF"}

response = requests.post(url, json=data)
result = response.json()

if result['status'] == 'active':
    m3u_url = result['m3u_url']
    print(f"تشغيل القنوات من: {m3u_url}")
else:
    print(f"خطأ: {result['message']}")
```

---

## 🎯 نظام النقاط

### تكلفة الخطط
- **سنة واحدة (1 نقطة):** 365 يوم
- **3 سنوات (2 نقاط):** 1095 يوم
- **10 سنوات (5 نقاط):** 3650 يوم

### كيفية العمل
1. المدير يضيف نقاط للموزع
2. الموزع يستخدم النقاط لتفعيل أجهزة
3. كل جهاز يستهلك نقاط حسب الخطة
4. النظام يتتبع جميع المعاملات

---

## ⚠️ المشاكل المعروفة

### 1. Network Error في النشر على Manus
**السبب:** قاعدة البيانات SQLite لا تعمل بشكل صحيح في البيئة المنشورة

**الحل:** النشر على Railway أو Render مع PostgreSQL

### 2. الموزعين لا يظهرون في القائمة
**السبب:** API لا يتصل بقاعدة البيانات بشكل صحيح

**الحل:** التأكد من إعدادات DATABASE_URL

### 3. علامة "Made with Manus"
**السبب:** النشر على منصة Manus المجانية

**الحل:** النشر على خدمة خارجية (Railway/Render)

---

## 📞 التواصل

واتساب: +1 (551) 430-5144

---

## 📄 الترخيص

جميع الحقوق محفوظة © 2025 Saba TV

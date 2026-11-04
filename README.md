# Goodreads

Bu loyiha Django framework asosida yaratilgan kitoblar va o'qish platformasi. Foydalanuvchilar kitoblar haqida ma'lumotlarni ko'rishi, ro'yxatdan o'tishi, tizimga kirishi va kitoblar bo'yicha sharhlar qoldirishi mumkin.

## Loyihani ishga tushirish

1. Virtual muhit yarating:

```bash
python -m venv venv
```

2. Virtual muhitni faollashtiring:

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Kerakli paketlarni o'rnating:

```bash
pip install -r requirements.txt
```

4. Ma'lumotlar bazasini tayyorlang va migratsiya qiling:

```bash
python manage.py migrate
```

5. Loyihani ishga tushiring:

```bash
python manage.py runserver
```

Loyiha default holda `http://127.0.0.1:8000/` manzilida ishlaydi.

## Proekt haqida qisqacha

- Django 4.1.5 asosida qurilgan
- `books` va `users` app'lari mavjud
- PostgreSQL ma'lumotlar bazasidan foydalaniladi
- Foydalanuvchi autentifikatsiyasi, kitoblar ro'yxati va sharhlar funksiyasi mavjud
- Frontend uchun Django template va static fayllar ishlatilgan

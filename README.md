# WordPress Category Matcher

این پروژه از Ollama برای دسته‌بندی خودکار پست‌های وردپرس بر اساس محتوای آنها استفاده می‌کند.

## پیش‌نیازها

- Docker و Docker Compose
- Git
- دسترسی به یک سایت وردپرس
- دسترسی به Ollama (محلی یا سرور)

## نصب و راه‌اندازی

1. کلون کردن مخزن:
```bash
git clone <repository-url>
cd WordPressProject
```

2. ساخت فایل `.env`:
```bash
# WordPress Configuration
WORDPRESS_URL=https://your-wordpress-site.com/wp-json/wp/v2
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-password

# Ollama Configuration
OLLAMA_MODEL=llama3:latest
OLLAMA_BASE_URL=http://localhost:11434

# Transformer Configuration
TRANSFORMER_MODEL=all-MiniLM-L6-v2
```

3. اجرای با Docker:
```bash
docker-compose up --build
```

## ساختار پروژه

- `main.py`: فایل اصلی برنامه
- `ollama_client.py`: کلاینت Ollama برای ارتباط با مدل
- `wordpress_client.py`: کلاینت وردپرس برای مدیریت پست‌ها و دسته‌بندی‌ها
- `category_matcher.py`: منطق تطبیق دسته‌بندی‌ها
- `utils.py`: توابع کمکی

## تنظیمات

### WordPress
- `WORDPRESS_URL`: آدرس API وردپرس
- `WORDPRESS_USERNAME`: نام کاربری وردپرس
- `WORDPRESS_PASSWORD`: رمز عبور وردپرس

### Ollama
- `OLLAMA_MODEL`: نام مدل Ollama (پیش‌فرض: llama3:latest)
- `OLLAMA_BASE_URL`: آدرس سرور Ollama (پیش‌فرض: http://localhost:11434)

### Transformer
- `TRANSFORMER_MODEL`: نام مدل Sentence Transformer (پیش‌فرض: all-MiniLM-L6-v2)

## نحوه کار

1. برنامه به وردپرس متصل می‌شود
2. پست‌های بدون دسته‌بندی را پیدا می‌کند
3. از Ollama برای پیشنهاد دسته‌بندی استفاده می‌کند
4. از Sentence Transformer برای تطبیق با دسته‌بندی‌های موجود استفاده می‌کند
5. دسته‌بندی‌های مناسب را به پست‌ها اضافه می‌کند

## نکات مهم

- فایل `.env` را در `.gitignore` قرار داده‌ایم و نباید در مخزن گیت قرار بگیرد
- برای امنیت بیشتر، از رمزهای عبور قوی استفاده کنید
- مطمئن شوید که سرور Ollama در دسترس است
- مدل‌های مورد نیاز در اولین اجرا دانلود می‌شوند

## عیب‌یابی

### خطای اتصال به Ollama
- مطمئن شوید که Ollama در حال اجراست
- آدرس `OLLAMA_BASE_URL` را بررسی کنید
- پورت 11434 باید در دسترس باشد

### خطای وردپرس
- اعتبارنامه‌های وردپرس را بررسی کنید
- مطمئن شوید که API وردپرس فعال است
- آدرس `WORDPRESS_URL` را بررسی کنید

### خطای مدل
- مطمئن شوید که مدل Ollama نصب شده است
- فضای کافی برای دانلود مدل‌ها داشته باشید
- اتصال اینترنت را بررسی کنید

## مشارکت

برای مشارکت در پروژه:
1. یک fork از مخزن ایجاد کنید
2. یک branch جدید بسازید
3. تغییرات خود را commit کنید
4. یک pull request ایجاد کنید

## لایسنس

MIT License 
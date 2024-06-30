# استفاده از تصویر رسمی Python
FROM python:3.9-slim

# تنظیم متغیر محیطی برای اطمینان از اینکه خروجی Python بدون بافر است
ENV PYTHONUNBUFFERED 1

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های مورد نیاز
COPY requirements.txt .
COPY spammer_bot.py .

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# اجرای ربات
CMD ["python", "spammer_bot.py"]

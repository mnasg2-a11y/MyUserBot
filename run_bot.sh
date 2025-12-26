#!/bin/bash

echo "🚀 تشغيل بوت تنصيب السورس..."

# التحقق من وجود المكتبات
pip install telethon python-dotenv aiohttp

# تشغيل البوت
python setup_bot.py

# في حال توقف البوت، إعادة التشغيل بعد 5 ثواني
while true; do
    echo "🔄 إعادة تشغيل البوت..."
    sleep 5
    python setup_bot.py
done

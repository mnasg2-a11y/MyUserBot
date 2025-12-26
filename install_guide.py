import os, subprocess, sys

def setup_bot():
    print("""
    ╔════════════════════════════════════════╗
    ║      🚀 إعداد بوت تنصيب السورس         ║
    ╚════════════════════════════════════════╝
    
    هذا الملف سيساعدك في إعداد بوت التنصيب.
    """)
    
    # 1. إنشاء بوت جديد
    print("\n1️⃣ **إنشاء بوت جديد على تليجرام:**")
    print("   - اذهب إلى @BotFather")
    print("   - أرسل /newbot")
    print("   - اختر اسم للبوت")
    print("   - اختر يوزر للبوت")
    print("   - انسخ التوكن")
    
    token = input("\n🔑 أدخل BOT_TOKEN: ").strip()
    
    # 2. الحصول على API_ID و API_HASH
    print("\n2️⃣ **الحصول على API_ID و API_HASH:**")
    print("   - اذهب إلى https://my.telegram.org")
    print("   - سجل الدخول بحسابك")
    print("   - اختر API Development Tools")
    print("   - أنشئ تطبيق جديد")
    print("   - انسخ API_ID و API_HASH")
    
    api_id = input("\n📱 أدخل API_ID: ").strip()
    api_hash = input("🔐 أدخل API_HASH: ").strip()
    
    # 3. تثبيت المكتبات
    print("\n3️⃣ **تثبيت المكتبات المطلوبة:**")
    packages = ['telethon', 'python-dotenv', 'aiohttp']
    
    for package in packages:
        print(f"   📦 جاري تثبيت {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ تم تثبيت {package}")
        except:
            print(f"   ❌ فشل تثبيت {package}")
    
    # 4. إنشاء ملف .env
    print("\n4️⃣ **إنشاء ملف الإعدادات:**")
    with open(".env", "w", encoding="utf-8") as f:
        f.write(f"BOT_TOKEN={token}\n")
        f.write(f"API_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
    
    print("   ✅ تم إنشاء ملف .env")
    
    # 5. إنشاء ملف users_data
    os.makedirs("users_data", exist_ok=True)
    os.makedirs("backups", exist_ok=True)
    
    with open("users_data/user_data.json", "w", encoding="utf-8") as f:
        f.write("{}")
    
    print("\n" + "="*50)
    print("✅ **تم الإعداد بنجاح!**")
    print("\n📋 **للتشغيل:**")
    print("   1. python setup_bot.py")
    print("   2. اذهب إلى البوت وابدأ بـ /start")
    print("\n🎯 **معلومات البوت:**")
    print(f"   - التوكن: {token[:10]}...")
    print(f"   - API_ID: {api_id}")
    print(f"   - API_HASH: {api_hash[:10]}...")
    print("="*50)

if __name__ == "__main__":
    setup_bot()

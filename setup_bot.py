import os, asyncio, zipfile, io, json, shutil, subprocess, sys, signal
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from dotenv import load_dotenv
import aiohttp

# تأكد من تثبيت المكتبات المطلوبة
REQUIRED_PACKAGES = [
    'telethon',
    'python-dotenv',
    'aiohttp'
]

# إعدادات البوت
BOT_TOKEN = os.getenv("BOT_TOKEN")  # سيتم إدخاله لاحقاً
API_ID = os.getenv("API_ID") or 1  # سيتم إدخاله لاحقاً
API_HASH = os.getenv("API_HASH") or ""

# إنشاء مجلدات التخزين
os.makedirs("users_data", exist_ok=True)
os.makedirs("backups", exist_ok=True)

# قاموس لتخزين بيانات المستخدمين
user_data = {}

# دالة لتحميل بيانات المستخدم
def load_user_data():
    global user_data
    try:
        with open("users_data/user_data.json", "r", encoding="utf-8") as f:
            user_data = json.load(f)
    except:
        user_data = {}

# دالة لحفظ بيانات المستخدم
def save_user_data():
    with open("users_data/user_data.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

# دالة لإنشاء ملف السورس - معدلة بدون أخطاء
def create_userbot_files(user_id):
    # إنشاء أرشيف ZIP
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # ملف main.py
        main_py_content = '''import os, asyncio, sys, importlib
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

# إعداد الجلسة
ENV_FILE = ".env"
if not os.path.exists(ENV_FILE):
    print("--- 🛠 إعداد البوت لأول مرة ---")
    api_id = input("أدخل API_ID: ")
    api_hash = input("أدخل API_HASH: ")
    with TelegramClient(StringSession(), api_id, api_hash) as temp:
        session_str = temp.session.save()
    with open(ENV_FILE, "w") as f:
        f.write(f"API_ID={api_id}\\nAPI_HASH={api_hash}\\nSTRING_SESSION={session_str}\\n")
    print("✅ تم الحفظ! أعد تشغيل البوت الآن.")
    exit()

load_dotenv(ENV_FILE)

# إنشاء العميل
client = TelegramClient(
    StringSession(os.getenv("STRING_SESSION")), 
    int(os.getenv("API_ID")), 
    os.getenv("API_HASH")
)

# دالة تحميل تلقائي لل plugins
def load_plugins():
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        print(f"⚠️ مجلد {plugins_dir} غير موجود! جاري إنشاؤه...")
        os.makedirs(plugins_dir)
        open(os.path.join(plugins_dir, "__init__.py"), "w").close()
        return
    
    loaded = 0
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                with open(os.path.join(plugins_dir, filename), "r", encoding="utf-8") as f:
                    exec(f.read(), {"client": client, "events": events})
                print(f"✅ تم تحميل: {filename}")
                loaded += 1
            except Exception as e:
                print(f"❌ خطأ في {filename}: {e}")
    
    return loaded

# أمر المساعدة
@client.on(events.NewMessage(outgoing=True, pattern=r'\\.مساعدة'))
async def help_handler(event):
    await event.edit("📋 **أوامر السورس:**\\n\\n"
                    "• `.فحص` - فحص البوت\\n"
                    "• `.ايدي` - معرفة الأيدي\\n"
                    "• `.معلومات` - معلومات البوت\\n"
                    "• `.مساعدة` - هذه القائمة\\n\\n"
                    "✨ **أضف ملفاتك في مجلد plugins**")

# أمر الفحص الأساسي
@client.on(events.NewMessage(outgoing=True, pattern=r'\\.فحص'))
async def ping_handler(event):
    await event.edit("✅ **السورس يعمل بشكل صحيح!**\\n\\n"
                    "تم التحميل من @YourSetupBot")

# أمر الأيدي
@client.on(events.NewMessage(outgoing=True, pattern=r'\\.ايدي'))
async def id_handler(event):
    await event.edit(f"👤 **ايديك هو:** `{event.sender_id}`")

async def main():
    print("🚀 جاري تشغيل اليوزربوت...")
    
    loaded = load_plugins()
    print(f"📂 تم تحميل {loaded} أمر من plugins")
    
    await client.start()
    me = await client.get_me()
    print(f"✅ البوت متصل: {me.first_name}")
    print("⏳ في انتظار الأوامر...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())'''
        
        zip_file.writestr("main.py", main_py_content)
        
        # ملف requirements.txt
        requirements_content = '''telethon==1.34.0
python-dotenv==1.0.0
aiohttp==3.9.1'''
        zip_file.writestr("requirements.txt", requirements_content)
        
        # ملف README.md
        readme_content = '''# 🚀 سورس اليوزربوت

تم تنصيب هذا السورس عبر بوت @YourSetupBot

## 📦 التثبيت:
1. قم بتثبيت المتطلبات:

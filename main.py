importimport os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

# اسم ملف الإعدادات
ENV_FILE = ".env"

def setup_env():
    """وظيفة لإعداد البيانات عند أول تشغيل"""
    if not os.path.exists(ENV_FILE):
        print("--- 🛠 إعداد البوت لأول مرة ---")
        api_id = input("أدخل API_ID الخاص بك: ")
        api_hash = input("أدخل API_HASH الخاص بك: ")
        
        # إنشاء عميل مؤقت لاستخراج الجلسة
        with TelegramClient(StringSession(), api_id, api_hash) as client:
            session_str = client.session.save()
            
        # حفظ البيانات في ملف .env
        with open(ENV_FILE, "w") as f:
            f.write(f"API_ID={api_id}\n")
            f.write(f"API_HASH={api_hash}\n")
            f.write(f"STRING_SESSION={session_str}\n")
        print("✅ تم حفظ البيانات بنجاح في ملف .env")

# تشغيل الإعداد التفاعلي
setup_env()

# تحميل البيانات من الملف
load_dotenv(ENV_FILE)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

# تشغيل البوت الفعلي
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def test(event):
    await event.edit("✅ البوت يعمل بنجاح مع الجلسة المحفوظة!")

print("🚀 اليوزربوت قيد التشغيل الآن...")
client.start()
client.run_until_disconnected()
 os
import glob
import importlib
from telethon import TelegramClient, events
from config import API_ID, API_HASH, STRING_SESSION

# إعداد العميل
client = TelegramClient(STRING_SESSION, API_ID, API_HASH)

def load_plugins():
    # البحث عن جميع ملفات الـ python داخل مجلد plugins
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        # استيراد الملف برمجياً
        plugin_name = name.replace("/", ".").replace("\\", ".").replace(".py", "")
        importlib.import_module(plugin_name)
        print(f"✅ تم تحميل الأمر: {plugin_name}")

print("🚀 جاري تشغيل اليوزربوت...")
load_plugins()

client.start()
client.run_until_disconnected()

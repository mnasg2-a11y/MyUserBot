import os, asyncio, glob, importlib
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# 1. إعداد الجلسة والبيانات
ENV_FILE = ".env"
if not os.path.exists(ENV_FILE):
    print("--- 🛠 إعداد البوت لأول مرة ---")
    api_id = input("أدخل API_ID: ")
    api_hash = input("أدخل API_HASH: ")
    with TelegramClient(StringSession(), api_id, api_hash) as temp:
        session_str = temp.session.save()
    with open(ENV_FILE, "w") as f:
        f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\nSTRING_SESSION={session_str}\n")
    print("✅ تم الحفظ! أعد تشغيل البوت الآن.")
    exit()

load_dotenv(ENV_FILE)
client = TelegramClient(
    StringSession(os.getenv("STRING_SESSION")), 
    int(os.getenv("API_ID")), 
    os.getenv("API_HASH")
)

# 2. وظيفة تحميل ملفات الـ plugins
def load_plugins():
    path = "plugins/*.py"
    files = glob.glob(path)
    for name in files:
        plugin_name = name.replace("/", ".").replace("\\\\", ".").replace(".py", "")
        importlib.import_module(plugin_name)
        print(f"✅ تم تحميل الأمر من الملف: {plugin_name}")

# إضافة: رفع ملفات ال plugins من المجلد بشكل صحيح
def load_plugins_fixed():
    for filename in os.listdir("plugins"):
        if filename.endswith(".py"):
            plugin_name = f"plugins.{filename[:-3]}"
            try:
                importlib.import_module(plugin_name)
                print(f"✅ تم تحميل: {plugin_name}")
            except Exception as e:
                print(f"❌ خطأ في تحميل {plugin_name}: {e}")

async def start_userbot():
    print("🚀 جاري تشغيل اليوزربوت...")
    load_plugins()  # الطريقة القديمة
    load_plugins_fixed()  # الطريقة الجديدة المضمونة
    await client.start()
    print("✅ البوت متصل الآن! جرب إرسال .فحص من حسابك.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(start_userbot())

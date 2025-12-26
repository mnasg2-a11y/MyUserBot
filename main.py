import os, asyncio, glob, importlib, sys
from telethon import TelegramClient, events
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

# إنشاء العميل
client = TelegramClient(
    StringSession(os.getenv("STRING_SESSION")), 
    int(os.getenv("API_ID")), 
    os.getenv("API_HASH")
)

# 2. إضافة أمر فحص أساسي هنا في main.py للتأكد
@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def main_ping_handler(event):
    await event.edit("✅ **جاري التشغيل من main.py مباشرة!**")

# 3. وظيفة تحميل ملفات الـ plugins
def load_plugins():
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        print(f"⚠️ مجلد {plugins_dir} غير موجود! جاري إنشاؤه...")
        os.makedirs(plugins_dir)
        return
    
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"plugins.{filename[:-3]}"
            try:
                # حذف النمط من الذاكرة أولاً إذا كان موجوداً
                if module_name in sys.modules:
                    del sys.modules[module_name]
                
                # استيراد الملف
                module = importlib.import_module(module_name)
                
                # إعادة تحميل للتأكد من التحديثات
                importlib.reload(module)
                
                print(f"✅ تم تحميل: {module_name}")
            except Exception as e:
                print(f"❌ خطأ في تحميل {module_name}: {e}")

async def start_userbot():
    print("🚀 جاري تشغيل اليوزربوت...")
    
    # تحميل الإضافات
    load_plugins()
    
    # بدء العميل
    await client.start()
    
    # الحصول على معلومات المستخدم
    me = await client.get_me()
    print(f"✅ البوت متصل الآن باسم: {me.first_name} (@{me.username})")
    print("📝 جرب إرسال الأوامر التالية في أي دردشة:")
    print("   • .فحص  - لفحص البوت")
    print("   • .ايدي - لمعرفة الأيدي")
    
    # تشغيل حتى الانقطاع
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(start_userbot())

import os, asyncio, importlib, sys, logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

# إعدادات اللوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# متغير لتخزين الأوامر المحملة
loaded_commands = {}

# 2. وظيفة تحميل الـ plugins
def load_plugins():
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        print(f"⚠️ مجلد {plugins_dir} غير موجود! جاري إنشاؤه...")
        os.makedirs(plugins_dir)
        return
    
    # مسح الكاش القديم
    for module_name in list(sys.modules.keys()):
        if module_name.startswith('plugins.'):
            del sys.modules[module_name]
    
    # تحميل كل ملف
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"plugins.{filename[:-3]}"
            try:
                # مسح الموديل من الذاكرة أولاً
                if module_name in sys.modules:
                    del sys.modules[module_name]
                
                # استيراد الملف
                spec = importlib.util.spec_from_file_location(
                    module_name, 
                    os.path.join(plugins_dir, filename)
                )
                module = importlib.util.module_from_spec(spec)
                
                # حقن العميل في namespace الموديل
                module.client = client
                
                # تنفيذ الموديل
                spec.loader.exec_module(module)
                
                # تسجيل الأوامر المحملة
                loaded_commands[filename] = module_name
                print(f"✅ تم تحميل: {module_name}")
                
            except Exception as e:
                print(f"❌ خطأ في تحميل {module_name}: {str(e)[:100]}")

# 3. أمر اختبار أساسي في main للتأكد
@client.on(events.NewMessage(outgoing=True, pattern=r'\.مين'))
async def test_handler(event):
    await event.edit("🔄 *جاري التشغيل من main.py*")

async def start_userbot():
    print("🚀 جاري تشغيل اليوزربوت...")
    
    # تحميل الإضافات
    load_plugins()
    
    # بدء العميل
    await client.start()
    
    # الحصول على معلومات المستخدم
    me = await client.get_me()
    print(f"\n✅ البوت متصل الآن باسم: {me.first_name} (@{me.username})")
    print(f"📊 عدد الأوامر المحملة: {len(loaded_commands)}")
    
    # عرض الأوامر المتاحة
    if loaded_commands:
        print("\n📋 الأوامر المتاحة من plugins:")
        for cmd in loaded_commands.keys():
            print(f"   • {cmd}")
    
    print("\n📝 جرب إرسال الأوامر التالية:")
    print("   .فحص  - لاختبار plugins")
    print("   .ايدي - لمعرفة الأيدي")
    print("   .مين  - لاختبار main.py")
    
    # إرسال رسالة تأكيد
    await client.send_message('me', '✅ *البوت يعمل الآن!*\n\nيمكنك استخدام الأوامر:'
                              '\n.فحص - للاختبار'
                              '\n.ايدي - لمعرفة الأيدي'
                              '\n.مين - للتأكد من التشغيل')
    
    print("\n⏳ في انتظار الأوامر...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(start_userbot())

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

# إنشاء العميل - مهم: قبل أي استيراد للملفات الأخرى
client = TelegramClient(
    StringSession(os.getenv("STRING_SESSION")), 
    int(os.getenv("API_ID")), 
    os.getenv("API_HASH")
)

# 2. وظيفة تحميل ملفات الـ plugins - معدلة
def load_plugins():
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        print(f"⚠️ مجلد {plugins_dir} غير موجود! جاري إنشاؤه...")
        os.makedirs(plugins_dir)
        return
    
    # قائمة الملفات المحملة
    loaded_plugins = []
    
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
                
                loaded_plugins.append(filename)
                print(f"✅ تم تحميل: {module_name}")
                
            except ImportError as e:
                print(f"⚠️ تحذير في {module_name}: {e}")
            except SyntaxError as e:
                print(f"❌ خطأ في تركيب {module_name}: {e}")
            except Exception as e:
                print(f"❌ خطأ في تحميل {module_name}: {e}")
    
    print(f"\n📂 إجمالي الملفات المحملة: {len(loaded_plugins)}")
    for plugin in loaded_plugins:
        print(f"   • {plugin}")

async def start_userbot():
    print("🚀 جاري تشغيل اليوزربوت...")
    
    # تحميل الإضافات
    load_plugins()
    
    # بدء العميل
    await client.start()
    
    # الحصول على معلومات المستخدم
    me = await client.get_me()
    print(f"\n✅ البوت متصل الآن باسم: {me.first_name} (@{me.username})")
    print("\n📝 جرب إرسال الأوامر التالية في أي دردشة:")
    print("   • .فحص     - فحص البوت من plugins")
    print("   • .ايدي    - معرفة الأيدي")
    print("   • .معلومات - معلومات البوت (إذا كان الملف موجوداً)")
    print("\n📌 ملاحظة: تأكد أنك ترسل الأوامر من حساب البوت نفسه!")
    
    # إظهار رسالة تأكيد
    async with client.conversation('me') as conv:
        await conv.send_message('🚀 **البوت يعمل الآن!**\n\n'
                              'يمكنك استخدام الأوامر:\n'
                              '.فحص - للتحقق\n'
                              '.ايدي - لمعرفة الأيدي')
    
    # تشغيل حتى الانقطاع
    print("\n⏳ في انتظار الأوامر...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(start_userbot())

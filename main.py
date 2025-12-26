import os, asyncio, sys, importlib, glob
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

# 2. قائمة لتخزين جميع الأوامر المحملة
loaded_commands = []

# 3. دالة تحميل تلقائي لكل الملفات
def load_plugins():
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        print(f"⚠️ مجلد {plugins_dir} غير موجود! جاري إنشاؤه...")
        os.makedirs(plugins_dir)
        open(os.path.join(plugins_dir, "__init__.py"), "w").close()
        return
    
    # مسح الموديولات القديمة من الذاكرة
    for module_name in list(sys.modules.keys()):
        if module_name.startswith('plugins.'):
            del sys.modules[module_name]
    
    # إنشاء namespace يحتوي على المتغيرات الأساسية
    plugin_namespace = {
        'client': client,
        'events': events,
        'TelegramClient': TelegramClient,
        'StringSession': StringSession,
        'asyncio': asyncio,
        'os': os,
        'sys': sys,
        'importlib': importlib
    }
    
    # تحميل كل ملف في plugins
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"plugins.{filename[:-3]}"
            file_path = os.path.join(plugins_dir, filename)
            
            try:
                # قراءة محتوى الملف
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # تنفيذ الكود في namespace مخصص
                exec(compile(code, file_path, 'exec'), plugin_namespace)
                
                # استخراج أنماط الأوامر من الملف
                patterns = extract_patterns_from_code(code)
                
                if patterns:
                    for pattern in patterns:
                        loaded_commands.append(pattern)
                
                print(f"✅ تم تحميل: {filename} ({len(patterns)} أمر)")
                
            except SyntaxError as e:
                print(f"❌ خطأ في بناء {filename}: {e}")
            except Exception as e:
                print(f"❌ خطأ في تحميل {filename}: {e}")

# 4. دالة لاستخراج أنماط الأوامر من الكود
def extract_patterns_from_code(code):
    patterns = []
    
    # البحث عن أنماط الأوامر في الكود
    lines = code.split('\n')
    for line in lines:
        line = line.strip()
        
        # البحث عن @client.on events.NewMessage
        if '@client.on' in line and 'pattern=' in line:
            try:
                # استخراج النمط من pattern=
                start = line.find('pattern=') + len('pattern=')
                end = line.find(',', start)
                if end == -1:
                    end = line.find(')', start)
                
                if start != -1 and end != -1:
                    pattern = line[start:end].strip()
                    # تنظيف النمط من r" " أو r' '
                    if pattern.startswith('r"') or pattern.startswith("r'"):
                        pattern = pattern[2:-1]
                    elif pattern.startswith('"') or pattern.startswith("'"):
                        pattern = pattern[1:-1]
                    
                    patterns.append(pattern)
            except:
                pass
    
    return patterns

# 5. أمر مساعدة تلقائي يعرض كل الأوامر
@client.on(events.NewMessage(outgoing=True, pattern=r'\.مساعدة'))
async def help_handler(event):
    if not loaded_commands:
        await event.edit("📭 **لا توجد أوامر محملة بعد**")
        return
    
    # تصنيف الأوامر
    commands_list = []
    for cmd in sorted(set(loaded_commands)):
        if cmd:  # تجاهل الأوامر الفارغة
            commands_list.append(f"• `{cmd}`")
    
    # تقسيم القائمة إلى أجزاء إذا كانت طويلة
    if len(commands_list) > 20:
        parts = [commands_list[i:i+20] for i in range(0, len(commands_list), 20)]
        for i, part in enumerate(parts):
            if i == 0:
                await event.edit(
                    f"📋 **جميع الأوامر المتاحة ({len(loaded_commands)} أمر):**\n\n" +
                    "\n".join(part) +
                    f"\n\n📄 الصفحة {i+1}/{len(parts)} - أرسل `.مساعدة {i+2}` للصفحة التالية"
                )
            else:
                await asyncio.sleep(0.5)
                await event.reply(
                    f"📋 **الصفحة {i+1}/{len(parts)}:**\n\n" +
                    "\n".join(part) +
                    f"\n\nأرسل `.مساعدة {i+2}` للصفحة التالية" if i+1 < len(parts) else ""
                )
    else:
        await event.edit(
            f"📋 **جميع الأوامر المتاحة ({len(loaded_commands)} أمر):**\n\n" +
            "\n".join(commands_list) +
            "\n\n✨ **تم التحميل تلقائياً من مجلد plugins**"
        )

# 6. أمر لفحص الملفات المحملة
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ملفات'))
async def files_handler(event):
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        await event.edit("📭 **مجلد plugins فارغ**")
        return
    
    files = []
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            size = os.path.getsize(os.path.join(plugins_dir, filename))
            files.append(f"📄 {filename} ({size} بايت)")
    
    await event.edit(
        f"📂 **الملفات في plugins ({len(files)} ملف):**\n\n" +
        "\n".join(files) if files else "📭 **لا توجد ملفات**"
    )

async def start_userbot():
    print("🚀 جاري تشغيل اليوزربوت...")
    
    # تحميل الإضافات تلقائياً
    print("📂 جاري تحميل الأوامر من plugins...")
    load_plugins()
    
    # بدء العميل
    await client.start()
    
    # الحصول على معلومات المستخدم
    me = await client.get_me()
    print(f"\n✅ البوت متصل الآن باسم: {me.first_name} (@{me.username})")
    
    # عرض إحصائيات
    print(f"📊 عدد الأوامر المحملة: {len(set(loaded_commands))}")
    print(f"📂 عدد الملفات في plugins: {len([f for f in os.listdir('plugins') if f.endswith('.py') and f != '__init__.py'])}")
    
    # عرض الأوامر الرئيسية فقط
    print("\n📝 **الأوامر الأساسية:**")
    print("   .مساعدة - عرض جميع الأوامر")
    print("   .ملفات   - عرض الملفات المحملة")
    print("   .فحص     - اختبار البوت")
    print("   .ايدي    - معرفة الأيدي")
    print("\n💡 **أضف أي ملف .py في مجلد plugins وسيتم تحميله تلقائياً**")
    
    # إرسال رسالة تأكيد
    try:
        await client.send_message(
            'me', 
            f'✅ **البوت يعمل الآن!**\n\n'
            f'👤 **اسم البوت:** {me.first_name}\n'
            f'📊 **عدد الأوامر:** {len(set(loaded_commands))}\n'
            f'📂 **الملفات:** {len([f for f in os.listdir("plugins") if f.endswith(".py")])}\n\n'
            f'📝 **استخدم:**\n'
            f'.مساعدة - لعرض جميع الأوامر\n'
            f'.ملفات - لعرض الملفات المحملة'
        )
    except:
        pass
    
    print("\n⏳ في انتظار الأوامر...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(start_userbot())

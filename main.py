import os
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

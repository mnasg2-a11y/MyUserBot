import os, asyncio, glob, importlib
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

ENV_FILE = ".env"

async def setup():
    if not os.path.exists(ENV_FILE):
        print("--- 🛠 إعداد البوت لأول مرة ---")
        api_id = input("أدخل API_ID: ")
        api_hash = input("أدخل API_HASH: ")
        async with TelegramClient(StringSession(), api_id, api_hash) as temp_client:
            session_str = temp_client.session.save()
            with open(ENV_FILE, "w") as f:
                f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\nSTRING_SESSION={session_str}\n")
        print("✅ تم الحفظ! أعد تشغيل السكريبت الآن بالأمر: python main.py")
        exit()

load_dotenv(ENV_FILE)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

def load_plugins():
    for f in glob.glob("plugins/*.py"):
        p_name = f.replace("/", ".").replace(".py", "")
        importlib.import_module(p_name)
        print(f"✅ تم تحميل الملحق: {p_name}")

async def start_bot():
    await setup()
    load_plugins()
    await client.start()
    print("🚀 اليوزربوت شغال الآن! جرب إرسال .فحص من حسابك.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(start_bot())

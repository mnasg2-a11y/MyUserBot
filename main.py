import os, asyncio, glob, importlib
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

ENV_FILE = ".env"

def setup():
    if not os.path.exists(ENV_FILE):
        print("--- 🛠 إعداد البوت لأول مرة ---")
        api_id = input("أدخل API_ID: ")
        api_hash = input("أدخل API_HASH: ")
        with TelegramClient(StringSession(), api_id, api_hash) as temp:
            session = temp.session.save()
        with open(ENV_FILE, "w") as f:
            f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\nSTRING_SESSION={session}\n")
        print("✅ تم الحفظ بنجاح!")

setup()
load_dotenv(ENV_FILE)

ID = int(os.getenv("API_ID"))
HASH = os.getenv("API_HASH")
SESS = os.getenv("STRING_SESSION")

client = TelegramClient(StringSession(SESS), ID, HASH)

def load_plugins():
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
    files = glob.glob("plugins/*.py")
    for name in files:
        p_name = name.replace("/", ".").replace("\\", ".").replace(".py", "")
        importlib.import_module(p_name)
        print(f"✅ تم تحميل: {p_name}")

async def run_bot():
    load_plugins()
    await client.start()
    print("🚀 البوت يعمل الآن! جرب إرسال .فحص")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(run_bot())

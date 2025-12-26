from telethon import events

# العميل سيكون متاحاً من خلال التحميل
try:
    from main import client
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
    from main import client

@client.on(events.NewMessage(outgoing=True, pattern=r'\.فحص'))
async def ping_handler(event):
    await event.edit("✅ **تمت الاستجابة بنجاح من داخل ملف الـ Plugins!**\n\n"
                    "السورس الآن يعمل بشكل صحيح من الـ plugins.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.ايدي'))
async def id_handler(event):
    await event.edit(f"👤 **ايديك هو:** `{event.sender_id}`")

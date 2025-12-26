from telethon import events
from main import client

@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def ping_handler(event):
    await event.edit("✅ **تمت الاستجابة بنجاح من داخل ملف الـ Plugins!**\n\nالسورس الآن يعمل بشكل صحيح.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.ايدي"))
async def id_handler(event):
    await event.edit(f"👤 **ايديك هو:** \`{event.sender_id}\`")

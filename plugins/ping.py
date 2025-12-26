from telethon import events
import __main__

client = __main__.client

@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def ping_handler(event):
    await event.edit("✅ **السورس شغال يا حسين!**\n\nتم التحميل من مجلد plugins بنجاح.")

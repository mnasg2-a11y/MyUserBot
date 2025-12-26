from telethon import events

@client.on(events.NewMessage(outgoing=True, pattern=r'\.test1'))
async def test1_handler(event):
    await event.edit("✅ هذا أمر جديد من test.py")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.test2'))
async def test2_handler(event):
    await event.edit("✅ أمر آخر من نفس الملف")

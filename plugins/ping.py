from main import client
from telethon import events
@client.on(events.NewMessage(outgoing=True, pattern=r"\.فحص"))
async def test(event):
    await event.edit("✅ **تم تحديث الحساب.. اليوزربوت شغال!**")

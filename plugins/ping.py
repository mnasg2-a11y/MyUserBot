from main import client
from telethon import events

@client.on(events.NewMessage(outgoing=True, pattern=r"\.بنج"))
async def ping(event):
    await event.edit("🚀 **شغال حبيبي!**")

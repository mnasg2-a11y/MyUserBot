@client.on(events.NewMessage(outgoing=True, pattern=r"\.معلومات"))
async def info_handler(event):
    me = await client.get_me()
    await event.edit(f"👤 **معلومات البوت:**\n"
                     f"• الاسم: {me.first_name}\n"
                     f"• اليوزر: @{me.username}\n"
                     f"• الأيدي: `{me.id}`")

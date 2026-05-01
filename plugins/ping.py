from telethon import events
import time

@events.register(events.NewMessage(pattern=r"\.بنك", outgoing=True))
async def ping(event):
    start = time.time()
    await event.edit("🏓")
    end = time.time()
    ms = round((end - start) * 1000, 2)
    await event.edit(f"**🏓 بونج!**\n**⏱ السرعة:** `{ms}ms`")

import os, asyncio, importlib, time                  from telethon import TelegramClient, events
                                                     # --- البيانات الأساسية ---
API_ID = 
API_HASH = ''
VERSION = "1.6"                                      GROQ_KEY = ""                                                                                          # متغيرات السيطرة
IS_POSTING = False
                                                     client = TelegramClient('manus_final_session', API_ID, API_HASH)
                                                     def load_plugins():
    plugins_path = "./plugins"                           if not os.path.exists(plugins_path): os.makedirs(plugins_path)                                            for filename in os.listdir(plugins_path):                if filename.endswith(".py") and not filename.startswith("__"):                                                try:                                                     importlib.import_module(f"plugins.{filename[:-3]}")                                                       print(f"✅ تم تحميل الإضافة: {filename}")
            except Exception as e:
                print(f"❌ خطأ في تحميل {filename}: {e}")                                                                                                      @client.on(events.NewMessage(pattern=r"\.فحص", outgoing=True))
async def check(event):                                  start = time.time()                                  await event.edit("🔄")
    ms = round((time.time() - start) * 1000, 2)          await event.edit(f"==================================\n|  اهلا بك في بوت كارديان \n\n|  سرعة السورس : `{ms}ms` \n|  أصدار السورس : `{VERSION}` \n|  المطور : @joh9n\n==================================")

@client.on(events.NewMessage(pattern=r"\.الاوامر", outgoing=True))                                        async def cmd_list(event):
    cliche_cmds = """
==================================                   |  قائمة أوامر سورس كارديان (V1.6) 🤖                                                                     | 🔹 `.فحص` : سرعة استجابة النظام.                   | 🔹 `.تفعيل النشر` : بدء النشر التلقائي.            | 🔹 `.تعطيل النشر` : إيقاف النشر التلقائي..         | 🔹 `.تفليش` : تنظيف الكروبات                       |                                                    |  المطور : @joh9n 👨‍💻
==================================                       """                                                  await event.edit(cliche_cmds)
                                                     async def main():                                        print("📡 جاري تشغيل سورس كارديان الصافي...")        load_plugins()
    await client.start()                                 print("✅ السورس شغال الآن بنظام الرقابة الشامل.")                                                        await client.run_until_disconnected()
                                                     if __name__ == '__main__':
    client.loop.run_until_complete(main())

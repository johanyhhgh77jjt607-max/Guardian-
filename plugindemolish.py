import asyncio, random, requests
from telethon import events
import __main__

# استخدمنا الـ ID للقناة لضمان وصول الرسائل بدون أخطاء اليوزر
target_chats = ["me", -1003791960777]

@__main__.client.on(events.NewMessage(pattern=r"\.تفعيل النشر", outgoing=True))
async def start_posting(event):
    if __main__.IS_POSTING:
        return await event.edit("⚠️ النشر مفعل بالفعل!")

    __main__.IS_POSTING = True
    await event.edit("بدء النشر التلقائي") # الكليشة اللي طلبتها

    while __main__.IS_POSTING:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {__main__.GROQ_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": "اكتب بيت شعر شعبي عراقي قصير وقوي مع إيموجي. بدون مقدمات."}]
            }

            response = requests.post(url, headers=headers, json=data)
            res_data = response.json()

            if response.status_code == 200 and 'choices' in res_data:
                ai_poem = res_data['choices'][0]['message']['content'].strip()
                for chat in target_chats:
                    if not __main__.IS_POSTING: break
                    try:
                        await __main__.client.send_message(chat, ai_poem)
                        await asyncio.sleep(18000)
                    except Exception as e:
                        print(f"⚠️ فشل النشر في {chat}: {e}")
            else:
                print(f"❌ Groq Error: {res_data}")

            # الانتظار ساعة واحدة (3600 ثانية)
            for _ in range(3600):
                if not __main__.IS_POSTING: break
                await asyncio.sleep(1)

        except Exception as e:
            print(f"❌ Error in poster: {e}")
            await asyncio.sleep(30)

@__main__.client.on(events.NewMessage(pattern=r"\.تعطيل النشر", outgoing=True))
async def stop_posting(event):
    __main__.IS_POSTING = False
    await event.edit("🛑 **تم إيقاف النشر بنجاح.**")

~/.../my_project/plugins $ ^C
~/.../my_project/plugins $ cat demolish.py
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import __main__

# أمر التفليش (طرد الكل)
@__main__.client.on(events.NewMessage(pattern=r"\.تفليش", outgoing=True))
async def demolish(event):
    if not event.is_group:
        return await event.edit("❌ **عزيزي، هذا الأمر مخصص للمجموعات فقط!**")

    await event.edit("🛠️ **بدأت عملية تنظيف الكروب (التفليش)...**")

    count = 0
    try:
        # جلب قائمة الأعضاء
        async for user in __main__.client.iter_participants(event.chat_id):
            # تخطي البوت نفسه وتخطي الحسابات المحذوفة لسرعة الكود
            if user.is_self or user.deleted:
                continue

            try:
                # حظر العضو (طرده)
                await __main__.client(EditBannedRequest(
                    event.chat_id,
                    user.id,
                    ChatBannedRights(until_date=None, view_messages=True)
                ))
                count += 1
            except Exception:
                # تخطي الأدمنية لأن ما تگدر تطردهم إذا أنت مو منشئ
                continue

        await event.edit(f"🔥 **تم تفليش الكروب بنجاح!**\n✅ تم طرد `{count}` عضو.")

    except Exception as e:
        await event.edit(f"❌ **حدث خطأ غير متوقع:**\n`{e}`")

# أمر لفك الحظر عن الكل (إرجاع الكروب) - إضافة من عندي
@__main__.client.on(events.NewMessage(pattern=r"\.تنظيف المحظورين", outgoing=True))
async def unban_all(event):
    if not event.is_group:
        return await event.edit("❌ للمجموعات فقط!")

    await event.edit("♻️ جاري مسح قائمة الحظر...")
    try:
        async for user in __main__.client.iter_participants(event.chat_id, filter=None):
            await __main__.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=False)))
        await event.edit("✅ تم مسح قائمة المحظورين.")
    except Exception as e:
        await event.edit(f"❌ خطأ: {e}")

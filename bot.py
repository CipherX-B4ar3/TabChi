import asyncio
from rubika import Client, methods, models, handlers, exceptions
import time
from random import choice as ch
import os.path
import logging
from re import findall
logging.basicConfig(level=logging.ERROR)

admin = ['u0DBCES0f3a0a8d079d01efad3172cf1', 'u0Dmt6L0ee28c1d9aa44394e4ffef5c9', 'u0DB3dK007d5b043bfdf082835e8ae6e']

async def main():
    async with Client(session="tabchi") as client:
        @client.on(handlers.MessageUpdates())
        async def tabchi(event):
            if event.raw_text == 'فور' and event.message.author_object_guid in admin:
                dialogs = await client(methods.chats.GetChats(start_id=None))
                if dialogs.chats:
                    total = len(dialogs.chats)
                    successful = 0
                    unsuccessful = 0
                    message = await event.reply(f'تعداد {total} چت پیدا شد شروع فرایند ارسال ...')
                    for index, dialog in enumerate(dialogs.chats, start=1):
                        if methods.groups.SendMessages in dialog.access:
                            try:
                                await event.forwards(dialog.object_guid, message_ids=event.reply_message_id)
                                successful += 1

                            except Exception:
                                unsuccessful += 1

                            progress = '|'
                            filled = int(index * 15 / total)
                            progress += '█' * filled
                            progress += '-' * (15 - filled)
                            progress += '| ▅▃▁' 
                            progress += f' [{int(index * 100 / total):,}%]'
        
                            await message.edit(
                                f'تعداد {index:,} چت از {total:,} چت بررسی شده است'
                                f'\nموفق : {successful:,}\nناموفق: {unsuccessful:,}\n\n{progress}'
                            )
                else:
                    await event.reply('در جستجوی چت ها با شکست مواجعه شد')        

        await client.run_until_disconnected()

asyncio.run(main())

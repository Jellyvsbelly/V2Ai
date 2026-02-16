import os
import asyncio
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL"]
YOUR_ID = int(os.environ["YOUR_ID"])

bot = Bot(token=BOT_TOKEN)

async def main():
    updates = await bot.get_updates()

    chat = await bot.get_chat(CHANNEL)

    results = []

    messages = await bot.get_chat_history(chat_id=chat.id, limit=10)

    for msg in messages:
        if msg.document and msg.document.file_name.endswith(".txt"):
            file = await bot.get_file(msg.document.file_id)
            path = await file.download_to_drive()

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("vless://") and line.endswith("🇮🇷"):
                        results.append(line)

            os.remove(path)

    with open("iran_vless.txt", "w", encoding="utf-8") as o:
        for r in results:
            o.write(r + "\n")

    await bot.send_document(chat_id=YOUR_ID, document=open("iran_vless.txt", "rb"))

asyncio.run(main())

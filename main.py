import os
import re
from telegram import Bot
from telegram.ext import ApplicationBuilder
from telegram.request import HTTPXRequest

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL"]
YOUR_ID = int(os.environ["YOUR_ID"])

bot = Bot(BOT_TOKEN)

async def main():
    updates = await bot.get_updates()

    files = []
    async for msg in bot.get_chat(CHANNEL).get_history(limit=10):
        if msg.document and msg.document.file_name.endswith(".txt"):
            file = await bot.get_file(msg.document.file_id)
            path = await file.download_to_drive()

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line=line.strip()
                    if line.startswith("vless://") and line.endswith("🇮🇷"):
                        files.append(line)

            os.remove(path)

    with open("iran_vless.txt","w",encoding="utf-8") as o:
        for f in files:
            o.write(f+"\n")

    await bot.send_document(chat_id=YOUR_ID, document=open("iran_vless.txt","rb"))

import asyncio
asyncio.run(main())

import os
import asyncio
from telethon import TelegramClient, events

from vc_engine.signaling import VCSignaling
from vc_engine.rtc_client import RTCClient
from vc_engine.player import AudioGenerator
from vc_engine.queue import MusicQueue

API_ID = 26969655
API_HASH = "f5be6abf55be85b2c11b77ca4a330cee"
BOT_TOKEN = "8480683100:AAHkbw_z77yyGBrxNc_cjY7LTszNyRBblNM"

bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
queue = MusicQueue()

@bot.on(events.NewMessage(pattern="/play"))
async def play_cmd(event):
    chat = event.chat_id
    text = event.message.text.split(" ", 1)

    if len(text) == 1:
        return await event.reply("Usage: /play filename.mp3")

    filename = text[1].strip()
    filepath = f"music/{filename}"

    if not os.path.exists(filepath):
        return await event.reply("File not found in /music folder")

    queue.add(filepath)
    await event.reply(f"Added to queue: {filename}")

    if hasattr(bot, "vc_busy"):
        return

    await start_player(chat)

async def start_player(chat_id):
    bot.vc_busy = True

    signaling = VCSignaling(bot)

    while True:
        song = queue.next()
        if not song:
            break

        gen = AudioGenerator(song)
        rtc = RTCClient(gen)

        offer = await rtc.create_offer()
        answer = await signaling.join(chat_id, offer)
        await rtc.set_answer(answer)

        await bot.send_message(chat_id, f"▶ Playing: {os.path.basename(song)}")

    bot.vc_busy = False

print("VC Music Bot Running...")
bot.run_until_disconnected()
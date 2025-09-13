import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import re

# ===== CONFIG =====
API_ID = "24196359"
API_HASH = "20a1b32381ed174799e8af8def3e176b"
BOT_TOKEN = "YOUR_BOT_TOKEN"

# ===== BOT INSTANCE =====
client = Client("ott_scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ===== INLINE BUTTON =====
update_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Updates", url="https://t.me/RDX_PVT_LTD")]]
)

# ===== COMMON FUNCTION =====
async def fetch_ott_data(api_url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

async def handle_ott_command(message: Message, api_url: str):
    msg = await message.reply("Fetching...")
    try:
        data = await fetch_ott_data(api_url)
        if not data:
            return await msg.edit_text("Failed to fetch data from API.")

        title = data.get("title") or "No Title"
        image_url = data.get("poster") or data.get("landscape")

        if not title and not image_url:
            return await msg.edit_text("No title or poster found for this URL.")

        text = (
            f"<b>{title}</b>\n\n"
            f"Poster: {image_url}\n\n"
            f"<b><blockquote>Powered By <a href='https://t.me/RDX_PVT_LTD'>RDX_PVT_LTD</a></blockquote></b>"
        )

        await msg.edit_text(
            text=text,
            disable_web_page_preview=False,
            reply_markup=update_button
        )

    except Exception as e:
        await msg.edit_text(f"Error: {e}")

# ===== OTT COMMAND HANDLERS =====
@client.on_message(filters.command(["sunnext", "hulu", "stage", "adda", "wetv", "plex", "iqiyi", "aha", "shemaroo", "apple"]))
async def ott_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide an OTT URL.\nExample:\n`/sunnext https://example.com`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://hgbots.vercel.app/bypaas/asa.php?url={ott_url}"
    await handle_ott_command(message, api_url)

@client.on_message(filters.command("airtel"))
async def airtel_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide an Airtel OTT URL.\nExample:\n`/airtel https://example.com`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://hgbots.vercel.app/bypaas/airtel.php?url={ott_url}"
    await handle_ott_command(message, api_url)

@client.on_message(filters.command("zee"))
async def zee_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide a Zee OTT URL.\nExample:\n`/zee https://example.com`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://hgbots.vercel.app/bypaas/zee.php?url={ott_url}"
    await handle_ott_command(message, api_url)

@client.on_message(filters.command("prime"))
async def prime_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide a Prime OTT URL.\nExample:\n`/prime https://example.com`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://primevideo.pbx1bots.workers.dev/?url={ott_url}"
    await handle_ott_command(message, api_url)

# Powered by @RDX_PVT_LTD
print("Bot is running...")
client.run()

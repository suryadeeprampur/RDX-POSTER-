import aiohttp
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import re
import os
from aiohttp import web

# ===== CONFIG =====
API_ID = "24196359"
API_HASH = "20a1b32381ed174799e8af8def3e176b"
BOT_TOKEN = "8310604285:AAG6xP6fpB7YL9FlpTY5gzN3ZRXqkXoPFrI"
CHANNEL_ID = "-1002959465580"
GROUP_ID = -4705647498  # Your group ID
MONGO_URI = "mongodb+srv://MovieClub:MovieClub@cluster0.dau2bnj.mongodb.net/MovieClub?retryWrites=true&w=majority&appName=Cluster0"

# ===== BOT INSTANCE =====
client = Client("ott_scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ===== INLINE BUTTON =====
update_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Updates", url="https://t.me/RDX_PVT_LTD")]]
)

# ===== DATABASE SETUP =====
db_client = MongoClient(MONGO_URI)
db = db_client.poster_bot
posters_collection = db.posters

# ===== AUTOMATIC POSTER SAVE IN CHANNEL =====
@client.on_message(filters.photo & filters.chat(CHANNEL_ID))
async def auto_save_poster(client, message: Message):
    try:
        if not message.caption:
            return

        url_match = re.search(r"(https?://\S+)", message.caption)
        if not url_match:
            await message.reply_text("No link found in caption. Please include a valid URL.")
            return

        link = url_match.group(1)
        name = message.caption.replace(link, "").strip()
        if not name:
            name = "Unnamed Poster"

        file_id = message.photo.file_id

        posters_collection.update_one(
            {"name": name},
            {"$set": {"link": link, "file_id": file_id}},
            upsert=True
        )

        print(f"Saved poster: '{name}' with link: {link}")

    except Exception as e:
        print(f"Error saving poster: {str(e)}")

# ===== RETRIEVE POSTER WITH /p COMMAND IN GROUP ONLY =====
@client.on_message(filters.command("p") & filters.chat(GROUP_ID))
async def get_poster(client, message: Message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply_text("Usage: /p <poster name>")
            return

        name = args[1].strip()
        result = posters_collection.find_one({"name": name})

        if result:
            file_id = result['file_id']
            link = result['link']
            await message.reply_photo(file_id, caption=f"Poster: {name}\nLink: {link}")
        else:
            await message.reply_text(f"No poster found for name '{name}'.")

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

# ===== LIST ALL POSTERS WITH /listposters IN GROUP ONLY =====
@client.on_message(filters.command("listposters") & filters.chat(GROUP_ID))
async def list_posters(client, message: Message):
    posters = posters_collection.find()
    names = [poster["name"] for poster in posters]

    if names:
        await message.reply_text("Saved Posters:\n" + "\n".join(names))
    else:
        await message.reply_text("No posters saved yet.")

# ===== OTT SCRAPER FUNCTIONS =====
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

# ===== OTT COMMAND HANDLERS (Group Only) =====
@client.on_message(filters.command(["sunnext", "hulu", "stage", "adda", "wetv", "plex", "iqiyi", "aha", "shemaroo", "apple"]) & filters.chat(GROUP_ID))
async def ott_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide an OTT URL.\nExample:\n`/sunnext https://example.com`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://hgbots.vercel.app/bypaas/asa.php?url={ott_url}"
    await handle_ott_command(message, api_url)

@client.on_message(filters.command("airtel") & filters.chat(GROUP_ID))
async def airtel_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide an Airtel OTT URL.\nExample:\n`/airtel https://example.com`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://hgbots.vercel.app/bypaas/airtel.php?url={ott_url}"
    await handle_ott_command(message, api_url)

@client.on_message(filters.command("zee") & filters.chat(GROUP_ID))
async def zee_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide a Zee OTT URL.\nExample:\n`/zee https://example.com`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://hgbots.vercel.app/bypaas/zee.php?url={ott_url}"
    await handle_ott_command(message, api_url)

@client.on_message(filters.command("prime") & filters.chat(GROUP_ID))
async def prime_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide a Prime OTT URL.\nExample:\n`/prime https://example.com`")

    ott_url = message.text.split(None, 1)[1].strip()
    api_url = f"https://primevideo.pbx1bots.workers.dev/?url={ott_url}"
    await handle_ott_command(message, api_url)

# Powered by @RDX_PVT_LTD
print("Bot is running...")
client.run()




async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)

port = int(os.environ.get("PORT", 8080))
web.run_app(app, host="0.0.0.0", port=port)

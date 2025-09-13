from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message
import re

# ===== CONFIG =====
API_ID = "24196359"
API_HASH = "20a1b32381ed174799e8af8def3e176b"
BOT_TOKEN = "8310604285:AAG6xP6fpB7YL9FlpTY5gzN3ZRXqkXoPFrI"
CHANNEL_ID = "-1002959465580"  # The channel where photos are posted
GROUP_ID = -4705647498  # Replace with your group chat ID (use negative for supergroups)
MONGO_URI = "mongodb+srv://MovieClub:MovieClub@cluster0.dau2bnj.mongodb.net/MovieClub?retryWrites=true&w=majority&appName=Cluster0"  # Your MongoDB URI

app = Client("hubcloud_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ===== DATABASE SETUP =====
client = MongoClient(MONGO_URI)
db = client.poster_bot
posters_collection = db.posters

# ===== AUTOMATIC POSTER SAVE IN CHANNEL =====
@app.on_message(filters.photo & filters.chat(CHANNEL_ID))
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
@app.on_message(filters.command("p") & filters.chat(GROUP_ID))
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

# ===== LIST POSTERS WITH /listposters IN GROUP ONLY =====
@app.on_message(filters.command("listposters") & filters.chat(GROUP_ID))
async def list_posters(client, message: Message):
    posters = posters_collection.find()
    names = [poster["name"] for poster in posters]

    if names:
        await message.reply_text("Saved Posters:\n" + "\n".join(names))
    else:
        await message.reply_text("No posters saved yet.")

# Powered by @RDX_PVT_LTD
print("Bot is running...")
app.run()

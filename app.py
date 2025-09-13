import os
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)

port = int(os.environ.get("PORT", 8080))
web.run_app(app, host="0.0.0.0", port=port)


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace with your own values
bot = Client(
    "bypass_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# -------- START COMMAND -------- #
@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    buttons = [
        [InlineKeyboardButton("📢 Channel", url="https://t.me/DD_Bypass_Updates")],
        [
            InlineKeyboardButton("📚 Help Commands", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("📩 Contact Us", url="https://t.me/YourUsername"),
            InlineKeyboardButton("💰 Donate Us", url="https://your.donate.link")
        ]
    ]

    await message.reply_photo(
        photo="https://telegra.ph/file/7e8c1d9a0d8c2278f5a34.jpg",  # Replace with your banner
        caption="🌹 Hey, I'm A Bypasser Bot Specially Coded For DD Botz",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# -------- CALLBACK HANDLER -------- #
@bot.on_callback_query()
async def callback_handler(client, query):
    if query.data == "help":
        await query.message.edit_caption(
            "📚 **Help Commands**\n\n"
            "`/start` - Start the bot\n"
            "`/bypass <link>` - Bypass supported links\n"
            "`/about` - Info about bot",
            reply_markup=query.message.reply_markup
        )

    elif query.data == "about":
        await query.message.edit_caption(
            "ℹ️ **About This Bot**\n\n"
            "🚀 I'm A Powerful Bypasser & File Tool Bot.\n"
            "✅ Maintained By DD Botz Team.\n"
            "⚡ Powered With Pyrogram.\n\n"
            "👨‍💻 Developer: @RDX1444\n"
            "📢 Updates: @DD_Bypass_Updates",
            reply_markup=query.message.reply_markup
        )


# -------- ADMIN START VERSION -------- #
@bot.on_message(filters.command("adminstart"))
async def admin_start(client, message):
    buttons = [
        [InlineKeyboardButton("📩 Contact Us", url="https://t.me/YourUsername")],
        [InlineKeyboardButton("💰 Donate Us", url="https://your.donate.link")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ]

    await message.reply_photo(
        photo="https://telegra.ph/file/7e8c1d9a0d8c2278f5a34.jpg",
        caption=(
            "🌹 We Regularly Maintain Our Bot To Avoid Errors And Irregularities.\n"
            "Our Bot Is Freely Available To Be Used In @DD_Bypass_Updates.\n\n"
            "If You Really Like Our Services Anyway Please Donate Any Amount "
            "Of Your Wish To Keep Bot Always Alive ❤️.\n\n"
            "Check Below Buttons For Admins."
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )


print("✅ Bot is running...")
bot.run()

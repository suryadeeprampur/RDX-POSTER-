import os
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)

port = int(os.environ.get("PORT", 8080))
web.run_app(app, host="0.0.0.0", port=port)

from telethon import events
import asyncio
from telethon.errors import MessageNotModifiedError

dep = []

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def restarter(event):
        if event.message.text == '-restart':
            try:
                await event.edit("Userbot restarting...")
                await asyncio.sleep(0.5)
            except MessageNotModifiedError:
                pass
            restart_userbot()

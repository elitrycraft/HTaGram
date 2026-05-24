from telethon import events

dep = []

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def restarter(event):
        if event.message.text == '-restart':
            await event.edit("Userbot restarting...")
            restart_userbot()

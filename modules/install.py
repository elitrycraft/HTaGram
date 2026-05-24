from telethon import events
import os, subprocess
import asyncio
import importlib
import sys
from contextlib import contextmanager
import io

dep = []

@contextmanager
def ignore_import_errors():
    try:
        yield
    except ImportError:
        pass

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def install_module(event):
        if event.message.text == '-install':
            reply = await event.get_reply_message()
            
            if reply and reply.file and reply.file.name.endswith('.py'):
                file_path = f"modules/{reply.file.name}"
                await reply.download_media(file_path)
                deps = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('dep = '):
                            deps = eval(line.split('=')[1].strip())
                            break
                if deps:
                    await event.edit(f"Installing dependencies for module {reply.file.name}...")
                    for deepend in deps:
                        process = await asyncio.create_subprocess_exec(sys.executable, "-m", "pip", "install", deepend)
                        await process.wait()
                        await event.edit(f"Installed {deepend} for module {reply.file.name}...")

                module = None
                with ignore_import_errors():
                    module = importlib.import_module(f"modules.{reply.file.name[:-3]}")
                await event.edit(f"Module {reply.file.name} installed. Restarting userbot.")
                await restart_userbot()
            else:
                await event.delete()

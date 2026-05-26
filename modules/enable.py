from telethon import events
import os
import json
from pathlib import Path
import asyncio
from telethon.errors import MessageNotModifiedError

dep = []
critical_modules = ["install.py", "uninstall.py", "restart.py", "disable.py", "enable.py", "modules.py"]
file_lock = asyncio.Lock()

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def enable_module(event):
        if event.message.text.startswith('-enable '):
            disabled_modules = []
            disabled_modules_path = Path('disabled_modules.json')

            if disabled_modules_path.is_file():
                async with file_lock:
                    with open("disabled_modules.json", "r", encoding="utf-8") as f:
                        try:
                            disabled_modules = json.load(f)
                        except json.JSONDecodeError:
                            disabled_modules = []
            
            module_name = event.message.text.split(' ')[1]

            if not module_name.endswith('.py'):
                module_name += '.py'

            module_name_path = Path(f"modules/{module_name}")

            if module_name in critical_modules:
                await event.edit(f"Module {module_name} not enabled, because it is a critical module for the userbot")
                return
            
            if module_name_path.is_file():
                if module_name in disabled_modules:
                    disabled_modules.remove(module_name)
                    async with file_lock:
                        with open("disabled_modules.json", "w", encoding="utf-8") as f:
                            json.dump(disabled_modules, f, ensure_ascii=False, indent=2)
                    try:
                        await event.edit(f"Module {module_name} enabled. Restarting userbot...")
                        await asyncio.sleep(0.5)
                    except MessageNotModifiedError:
                        pass
                    restart_userbot()
                else:
                    await event.edit(f"Module {module_name} is not disabled")
            else:
                await event.edit(f"Module {module_name} not found")

from telethon import events
import os
import json
from pathlib import Path
from telethon.errors import MessageNotModifiedError
import asyncio

dep = []
critical_modules = ["install.py", "uninstall.py", "restart.py", "disable.py", "enable.py", "modules.py"]
file_lock = asyncio.Lock()

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def disable_module(event):
        if event.message.text.startswith('-disable '):
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
                await event.edit(f"Module {module_name} not disabled, because it is a critical module for the userbot")
                return
            
            if module_name_path.is_file():
                if module_name not in disabled_modules:
                    disabled_modules.append(module_name)
                    async with file_lock:
                        with open("disabled_modules.json", "w", encoding="utf-8") as f:
                            json.dump(disabled_modules, f, ensure_ascii=False, indent=2)
                    try:
                        await event.edit(f"Module {module_name} disabled. Restarting userbot...")
                        await asyncio.sleep(0.5)
                    except MessageNotModifiedError:
                        pass
                    restart_userbot()
                else:
                    await event.edit(f"Module {module_name} is already disabled")
            else:
                await event.edit(f"Module {module_name} not found")

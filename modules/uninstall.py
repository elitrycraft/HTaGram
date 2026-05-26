from telethon import events
import os
import json
from pathlib import Path
import asyncio
from telethon.errors import MessageNotModifiedError

critical_modules = ["install.py", "uninstall.py", "restart.py", "disable.py", "enable.py", "modules.py"]
dep = []
file_lock = asyncio.Lock()

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def uninstall_module(event):
        disabled_modules = []
        disabled_modules_path = Path('disabled_modules.json')
        if disabled_modules_path.is_file():
            async with file_lock:
                with open("disabled_modules.json", "r", encoding="utf-8") as f:
                    try:
                        disabled_modules = json.load(f)
                    except json.JSONDecodeError:
                        disabled_modules = []
        if event.message.text.startswith('-uninstall '):
            module_name = event.message.text.split(' ')[1]
            if not module_name.endswith('.py'):
                module_name += '.py'

            if module_name in critical_modules:
                await event.edit(f"Module {module_name} not uninstalled, because is critical module for userbot")
                return
            
            file_path = f"modules/{module_name}"
            
            if os.path.exists(file_path):
                if module_name in disabled_modules: disabled_modules.remove(module_name)
                with open("disabled_modules.json", "w", encoding="utf-8") as f:
                    json.dump(disabled_modules, f, ensure_ascii=False, indent=2)
                os.remove(file_path)
                try:
                    await event.edit(f"Module {module_name} uninstalled. Restarting userbot")
                    await asyncio.sleep(0.5)
                except MessageNotModifiedError:
                    pass
                restart_userbot()
            else:
                await event.edit(f"Module {module_name} not found")

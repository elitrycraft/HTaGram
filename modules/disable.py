from telethon import events
import os
import json
from pathlib import Path

dep = []
critical_modules = ["install.py", "uninstall.py", "restart.py", "disable.py", "enable.py"]

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def disable_module(event):
        if event.message.text.startswith('-disable '):
            disabled_modules = []
            disabled_modules_path = Path('disabled_modules.json')

            if disabled_modules_path.is_file():
                with open("disabled_modules.json", "r", encoding="utf-8") as f:
                    disabled_modules = json.load(f)
            
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
                    with open("disabled_modules.json", "w", encoding="utf-8") as f:
                        json.dump(disabled_modules, f, ensure_ascii=False, indent=2)
                    await event.edit(f"Module {module_name} disabled. Restarting userbot...")
                    restart_userbot()
                else:
                    await event.edit(f"Module {module_name} is already disabled")
            else:
                await event.edit(f"Module {module_name} not found")

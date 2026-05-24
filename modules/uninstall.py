from telethon import events
import os

critical_modules = ["install.py", "uninstall.py", "restart.py", "disable.py", "enable.py"]
dep = []

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def uninstall_module(event):
        if event.message.text.startswith('-uninstall '):
            module_name = event.message.text.split(' ')[1]
            if not module_name.endswith('.py'):
                module_name += '.py'

            if module_name in critical_modules:
                await event.edit(f"Module {module_name} not uninstalled, because is critical module for userbot")
                return
            
            file_path = f"modules/{module_name}"
            
            if os.path.exists(file_path):
                os.remove(file_path)
                await event.edit(f"Module {module_name} uninstalled. Restarting userbot")
                restart_userbot()
            else:
                await event.edit(f"Module {module_name} not found")

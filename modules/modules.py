from telethon import events
import os
import json
from telethon.errors import MessageNotModifiedError

dep = []

async def run(client, restart_userbot):
    @client.on(events.NewMessage(outgoing=True))
    async def modules_list(event):
        if event.message.text == '-modules':
            modules = [f[:-3] for f in os.listdir("modules") if f.endswith('.py') and f != '__init__.py']
            
            if not modules:
                await event.edit("No modules found")
                return
            
            # Загружаем список отключенных модулей
            disabled_modules = []
            if os.path.exists("disabled_modules.json"):
                with open("disabled_modules.json", 'r') as f:
                    try:
                        disabled_modules = json.load(f)
                    except json.JSONDecodeError:
                        disabled_modules = []
                # Приводим к единому формату (без .py)
                disabled_modules = [m.replace('.py', '') for m in disabled_modules]
            
            # Формируем список с статусом
            modules_list = []
            for module_name in modules:
                status = "Disabled" if module_name in disabled_modules else "Enabled"
                modules_list.append(f"├ `{module_name}` - {status}")
            
            output = "**📚 Modules:**\n" + "\n".join(modules_list)
            await event.edit(output, parse_mode='markdown')

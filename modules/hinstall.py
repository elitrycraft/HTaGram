from telethon import events
import os, subprocess
import asyncio
import importlib
import sys
from contextlib import contextmanager
import io
import ast
from telethon.errors import MessageNotModifiedError
import requests

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
        if event.message.text.startswith('-hinstall'):
            parts = event.message.text.split()
            if len(parts) < 2:
                await event.edit("Usage: -hinstall <module_name>")
                return
                
            module_name = parts[1]
            if not module_name.endswith('.py'):
                module_name += '.py'

            github_url = f"https://raw.githubusercontent.com/elitrycraft/HTaGram_modules/refs/heads/main/modules/{module_name}"
            
            await event.edit(f"Downloading module {module_name} from GitHub...")
            
            try:
                response = requests.get(github_url)
                response.raise_for_status()
                
                # Save the module
                file_path = f"modules/{module_name}"
                os.makedirs("modules", exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                deps = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('dep = '):
                            try:
                                deps = ast.literal_eval(line.split('=')[1].strip())
                            except:
                                deps = []
                            break
                if deps:
                    await event.edit(f"Installing dependencies for module {module_name}...")
                    for deepend in deps:
                        process = await asyncio.create_subprocess_exec(
                            sys.executable, "-m", "pip", "install", deepend
                        )
                        await process.wait()
                        await event.edit(f"Installed {deepend} for module {module_name}...")
                
                await event.edit(f"Module {module_name} installed successfully! Restarting userbot...")
                await asyncio.sleep(0.5)
                await restart_userbot()
                
            except requests.exceptions.RequestException as e:
                await event.edit(f"Failed to download module: {str(e)}")
            except Exception as e:
                await event.edit(f"Error installing module: {str(e)}")
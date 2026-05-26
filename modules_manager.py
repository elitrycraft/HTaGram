import os
import importlib
import asyncio
from pathlib import Path
import json

file_lock = asyncio.Lock()

async def load_modules(client, restart_userbot):
    modules_dir = Path(__file__).parent / 'modules'
    tasks = []
    disabled_modules = []
    disabled_modules_path = Path('disabled_modules.json')
    if disabled_modules_path.is_file():
        async with file_lock:
            with open("disabled_modules.json", "r", encoding="utf-8") as f:
                try:
                    disabled_modules = json.load(f)
                except json.JSONDecodeError:
                    disabled_modules = []
            
    
    for file in modules_dir.iterdir():
        if file.suffix == '.py' and file.name != '__init__.py' and file.name != 'main.py':
            module_name = file.stem
            if file.name in disabled_modules:
                print(f"Module is not loaded {module_name}, because it's disabled")
                continue
            try:
                module = importlib.import_module(f'modules.{module_name}')
                if hasattr(module, 'run'):
                    print(f"Module is loaded {module_name}")
                    task = asyncio.create_task(module.run(client, restart_userbot))
                    tasks.append(task)
            except Exception as e:
                print(f"Error in {module_name}: {e}")
    
    if tasks:
        await asyncio.gather(*tasks)

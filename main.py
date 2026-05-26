import telethon
import requests
from pathlib import Path
import sys, os
import sqlite3
import warnings
import asyncio
import subprocess
warnings.filterwarnings("ignore", category=UserWarning, module="telethon")

api_id = None
api_hash = None

art = """
█   █ █████  ███   ███  ████   ███  █   █ 
█   █   █   █   █ █     █   █ █   █ ██ ██ 
█████   █   █████ █  ██ ████  █████ █ █ █ 
█   █   █   █   █ █   █ █  █  █   █ █   █ 
█   █   █   █   █  ███  █   █ █   █ █   █
"""

print(art)

print("\n")
print("API ID and API HASH can be obtained from my.telegram.org")
os.system("title HTaGram")

api_id_path = Path('api_id.txt')
api_hash_path = Path('api_hash.txt')

if api_id_path.is_file() and api_hash_path.is_file():
    print("Saved API values found")
    with open('api_id.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        api_id = int(content)
        print(f"API ID: {api_id}")
    with open('api_hash.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        api_hash = str(content)
        print(f"API HASH: {api_hash}")
else:
    print("Saved API values not found")
    api_id = int(input("Write API ID: "))

    api_hash = str(input("Write API HASH: "))

    with open("api_id.txt", "w", encoding="utf-8") as file:
        file.write(str(api_id))


    with open("api_hash.txt", "w", encoding="utf-8") as file:
        file.write(api_hash)

    print("API values are saved")

tg_client = None

def restart_userbot():
    subprocess.Popen([sys.executable] + sys.argv)
    os._exit(0)

async def ConnectToTelegram():
    global tg_client
    client = telethon.TelegramClient('HTGRAN CLIENT', api_id, api_hash)
    await client.start()
    tg_client = client
    import modules_manager
    await modules_manager.load_modules(client, restart_userbot)
    await client.run_until_disconnected()

asyncio.run(ConnectToTelegram())

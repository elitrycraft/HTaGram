import telethon
import requests
from pathlib import Path
import sys, os
import sqlite3
import warnings
import asyncio
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
        file.write(api_id)


    with open("api_hash.txt", "w", encoding="utf-8") as file:
        file.write(api_hash)

    print("API values are saved")

def check_telegram():
    url = "https://telegram.org"
    
    try:
        response = requests.get(url, timeout=5)

        if response.status_code < 400:
            return True
        else:
            return False
            
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    except requests.RequestException as e:
        return False

tg_client = None

def restart_userbot():
    python = sys.executable
    os.execl(python, python, *sys.argv)

if check_telegram() == True:
    print("Direct connection to Telegram successful")
    with telethon.TelegramClient('HTGRAN CLIENT', api_id, api_hash) as client:
        tg_client = client
        import modules_manager
        client.loop.run_until_complete(modules_manager.load_modules(client, restart_userbot))
        client.run_until_disconnected()
else:
    print("Direct connection to Telegram is unsuccessful")


while True:
    try:
        pass
    except KeyboardInterrupt:
        break

import os, subprocess, zipfile, asyncio, platform
from datetime import datetime
from telethon import TelegramClient, events
from giturlparse import parse
from urllib.parse import urlparse
import requests

# Replace with your credentials
API_ID, API_HASH, BOT_TOKEN = 'your_api_id', 'your_api_hash', 'your_bot_token'
REPO_DIR = 'tmp'
os.makedirs(REPO_DIR, exist_ok=True)

client = TelegramClient('TeleGitz', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
START_TIME = datetime.now()

async def handle_message(event):
    if event.text.startswith(('/start', '/uptime')):
        if event.text.startswith('/start'):
            await event.respond('TeleGitz v2.0 - A Telegram Git cloner\nAuthor: https://github.com/danii-saahir\nUsage: Send any Git repo URL')
        elif event.text.startswith('/uptime'):
            uptime = await get_uptime()
            response_message = await event.respond(f'TeleGitz Uptime: {uptime}')
            await asyncio.sleep(5)
            await client.delete_messages(event.chat_id, [event.id, response_message.id])
    elif event.text.startswith(('http://', 'https://')):
        parsed_url = urlparse(event.text)
        if parsed_url.scheme and parsed_url.netloc:
            git_url = parse(event.text)
            if git_url and git_url.host and git_url.repo:
                await clone_and_send(event.text, event)
            else:
                await event.respond('Invalid Git repo URL. Please provide a valid Git repo URL.')
        else:
            await event.respond('Invalid URL. Please provide a valid Git repo URL.')
    else:
        await event.respond('Invalid URL format. Please check and try again.')

async def get_uptime():
    uptime = datetime.now() - START_TIME
    return str(uptime).split('.')[0]

async def clone_and_send(url, event):
    try:
        git_url = parse(url)
        if git_url and git_url.host and git_url.repo:
            repo_exists = check_repo_existence(git_url)
            if repo_exists:
                clone_message = await event.respond('Cloning repo...')
                repo_name = os.path.splitext(os.path.basename(url))[0]
                repo_path, zip_filename = os.path.join(REPO_DIR, repo_name), f'{repo_name}.zip'

                subprocess.run(['git', 'clone', url, repo_path])

                with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                    for root, _, files in os.walk(repo_path):
                        for file in files:
                            zip_file.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), repo_path))

                subprocess.run(['rm', '-rf', repo_path])

                await client.delete_messages(event.chat_id, [clone_message.id])

                upload_message = await event.respond('Uploading ZIP to Telegram...')
                await client.send_file(event.chat_id, zip_filename, caption='Success! Download or forward ZIP.')
                os.remove(zip_filename)

                await client.delete_messages(event.chat_id, [upload_message.id])
            else:
                await event.respond('The requested Git repository does not exist. Please provide a valid Git repo URL.')
        else:
            await event.respond('Invalid Git repo URL. Please provide a valid Git repo URL.')
    except subprocess.CalledProcessError:
        await event.respond('An error occurred during the cloning process. Please try again.')

def check_repo_existence(git_url):
    api_url = f'https://{git_url.host}/{git_url.owner}/{git_url.repo}'
    response = requests.get(api_url)
    return response.status_code == 200

async def display_uptime():
    while True:
        clear_terminal()
        uptime = await get_uptime()
        print(f"TeleGitz Uptime: {uptime}")
        await asyncio.sleep(5)

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

client.on(events.NewMessage)(handle_message)
client.loop.create_task(display_uptime())
client.run_until_disconnected()

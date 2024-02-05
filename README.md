# TeleGitz
Telegram bot for cloning Git repo, supports any Git provider.

## Features
- Automatically sends cloned Git repo as a ZIP file to the user.
- Bot uptime tracking.
- Supports any Git providers.
- Automatically deletes temporarily stored Git repos in system.

## Setup
1. **Telegram API Credentials:**
   - Go to [Telegram API platform](https://my.telegram.org/auth).
   - Create an app and obtain the `api_id` and `api_hash`.

2. **Telegram Bot Token:**
   - Chat with "BotFather" on Telegram.
   - Use the `/newbot` command to get the `bot_token`.

Replace these credentials in the Python script.

## Requirements
1. Python3
2. Pip
3. Git

## Deployment (Terminal)
```bash
  git clone https://github.com/danii-saahir/TeleGitz
  pip install telethon giturlparse requests
  cd TeleGitz
  python3 telegitz.py
```

## Usage (Telegram Bot)
1. Send `/start` to your bot.
2. Send any Git repo URL and receive the ZIP file.
3. Send `/uptime` to get bot uptime.

## Bugs, problems etc.
- It is highly expected as this project is using a simple code base, there is so much more to improve, feel free to contribute/PR or open issues.

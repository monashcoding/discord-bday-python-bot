# Discord Birthday Python Bot

A Python bot that checks a Notion database for member birthdays and sends a celebratory message to a Discord channel via webhook.

## Environment Variables

See `.env.example` for required variables.

- `NOTION_TOKEN`: Notion integration token
- `DATABASE_ID`: Notion database ID
- `WEBHOOK_URL`: Discord webhook URL
- `HR_DISCORD_ID`: Discord HR role ID to tag

## Features

- Fetches member data from Notion.
- Checks if today is any member’s birthday.
- Sends a Discord message tagging the HR role for each birthday.

## Requirements

- Python 3.9+
- Notion integration and database
- Discord webhook URL

## Setup

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd discord-bday-python-bot
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your values.

5. **Run locally:**
   ```sh
   python main.py
   ```


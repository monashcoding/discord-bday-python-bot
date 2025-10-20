import logging
import os
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

from apis.discord_api import send_discord_message
from apis.notion_api import get_all_notion_pages
from utils.utils import is_active_mac_member, is_today_their_birthday

# Load environment variables from .env if present
load_dotenv()

logging.basicConfig(level=logging.INFO)

def main():
    melbourne_tz = ZoneInfo("Australia/Melbourne")
    now = datetime.now(melbourne_tz)
    logging.info(f"Birthday bot started at {now.isoformat()}")

    # --- DST-safe midnight alignment ---
    # If the bot runs before local midnight (AEST period), wait until midnight.
    # If it runs after midnight (AEDT period), continue immediately.
    target_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if now < target_midnight:
        # we're before midnight today → run at today's midnight
        pass
    else:
        # already past today's midnight → run next midnight
        target_midnight += timedelta(days=1)

    wait_seconds = (target_midnight - now).total_seconds()
    if wait_seconds > 0 and wait_seconds < 86400:  # sanity guard
        logging.info(f"Waiting {wait_seconds/3600:.2f} hours until local midnight...")
        time.sleep(wait_seconds)
    else:
        logging.info("Already past local midnight — continuing immediately.")
    # -----------------------------------

    # Once it’s at or after local midnight, proceed as usual
    today = datetime.now(melbourne_tz)
    current_month_day = today.strftime("%m-%d")

    # Retrieve environment variables
    NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
    DATABASE_ID = os.environ.get('DATABASE_ID')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
    HR_DISCORD_ID = os.environ.get('HR_DISCORD_ID')

    if not all([NOTION_TOKEN, DATABASE_ID, WEBHOOK_URL, HR_DISCORD_ID]):
        logging.error("One or more environment variables are not set. Please check NOTION_TOKEN, DATABASE_ID, WEBHOOK_URL, HR_DISCORD_ID.")
        return

    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    people_with_birthdays = []

    # Get all pages from Notion
    pages = get_all_notion_pages(DATABASE_ID, headers)
    logging.info(f"Fetched {len(pages)} pages from Notion database.")

    for page in pages:
        # Check if the person is an active MAC member
        if not is_active_mac_member(page):
            continue

        # Check if today is their birthday
        person_name = page["properties"].get("Name", {}).get("title", [{}])[0].get("text", {}).get("content")
        if person_name and is_today_their_birthday(page, current_month_day):
            people_with_birthdays.append(person_name)
        elif not person_name:
            logging.warning(f"Could not find name for a page with potential birthday on page ID: {page.get('id')}")

    # Send out a message for every person that has a birthday
    if not people_with_birthdays:
        logging.info("No birthdays today. No messages sent.")
        return

    for person in people_with_birthdays:
        send_discord_message(WEBHOOK_URL, HR_DISCORD_ID, person)

    logging.info('Birthday bot completed.')

if __name__ == "__main__":
    main()

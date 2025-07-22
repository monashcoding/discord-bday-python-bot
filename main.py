import logging
import os
from datetime import datetime
import azure.functions as func

from apis.discord_api import send_discord_message
from apis.notion_api import get_all_notion_pages
from utils.utils import is_active_mac_member, is_today_their_birthday
from zoneinfo import ZoneInfo

# for local testing
from dotenv import load_dotenv
load_dotenv()

# Configure logging for Azure Functions
logging.basicConfig(level=logging.INFO)

def main(mytimer: func.TimerRequest) -> None:
    melbourne_tz = ZoneInfo("Australia/Melbourne")
    today = datetime.now(melbourne_tz)
    current_month_day = today.strftime("%m-%d")

    if mytimer.past_due:
        logging.warning('The timer is past due! Function ran at %s', today.isoformat())

    logging.info('Python timer trigger function started at %s', today.isoformat())

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
        # Check if the person is an active MAC member based on 'Current MAC Role'
        if not is_active_mac_member(page):
            continue

        # Check if today is their birthday
        person_name = page["properties"].get("Name", {}).get("title", [{}])[0].get("text", {}).get("content")
        if person_name and is_today_their_birthday(page, current_month_day):
            people_with_birthdays.append(person_name)
        elif not person_name:
            logging.warning(f"Could not find name for a page with potential birthday on page ID: {page.get('id')}")

    # Send out a message for every person that has a birthday!
    if not people_with_birthdays:
        logging.info("No birthdays today. No messages sent.")
        return

    for person in people_with_birthdays:
        send_discord_message(WEBHOOK_URL, HR_DISCORD_ID, person)

    logging.info('Python timer trigger function completed.')

if __name__ == "__main__":
    class DummyTimer:
        past_due = False
    main(DummyTimer())
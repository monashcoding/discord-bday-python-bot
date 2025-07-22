import requests
import logging

def send_discord_message(webhook_url: str, hr_discord_id: str, person_name: str):
    discord_payload = {
        "content": f"<@&{hr_discord_id}>",
        "embeds": [
            {
                "title": "Birthday Alert!",
                "description": f"Today is {person_name}'s birthday! 🎉",
                "color": 0xffe430
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=discord_payload)
        response.raise_for_status()
        logging.info(f"Successfully sent birthday message for {person_name}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending Discord webhook for {person_name}: {e}")


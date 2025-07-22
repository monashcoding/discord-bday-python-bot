import requests
import logging


def get_all_notion_pages(database_id: str, headers: dict) -> list:
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    all_results = []
    has_more = True
    start_cursor = None
    page_size = 100 # Default page size for Notion API, often optimal

    while has_more:
        payload = {"page_size": page_size}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching Notion pages: {e}")
            break # Exit loop on error

        all_results.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    return all_results


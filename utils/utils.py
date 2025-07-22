import logging

def is_active_mac_member(page: dict) -> bool:
    """
    Determines if a person is an active MAC member based on their 'Current MAC Role'.
    'Alumni' or blank roles are considered non-active.
    """
    mac_role_prop = page["properties"].get('Current MAC Role')
    if mac_role_prop and mac_role_prop.get("select"):
        role_name = mac_role_prop["select"].get("name")
        if role_name and role_name.lower() != "alumni":
            return True
    elif not mac_role_prop or not mac_role_prop.get("select") or not mac_role_prop["select"].get("name"):
        # Treat blank/missing 'Current MAC Role' as non-active
        person_name = page["properties"].get("Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown Name")
        logging.info(f"Page (Name: {person_name}) has blank or missing 'Current MAC Role', treating as non-active.")
        return False
    return False

def is_today_their_birthday(page: dict, current_month_day: str) -> bool:
    """
    Checks if today is the person's birthday based on the 'Birthday' property.
    """
    bday_prop = page["properties"].get("Birthday")
    if not bday_prop or not bday_prop.get("date"):
        return False # Skip if birthday property or date is missing

    bday_start_str = bday_prop["date"]["start"]
    try:
        # Extract MM-DD from the birthday string (assumes YYYY-MM-DD format)
        birthday_month_day = bday_start_str[-5:]
        return birthday_month_day == current_month_day
    except IndexError:
        logging.warning(f"Birthday date format unexpected for page ID {page.get('id')}: {bday_start_str}")
        return False


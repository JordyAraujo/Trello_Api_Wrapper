from typing import Dict

from ..trello_requests import get_request, was_successful


def fetch_data(card) -> Dict[str, str]:
    """Loads CardList information."""
    url = f"https://api.trello.com/1/cards/{card.id}"
    response = get_request(card, url)
    if was_successful(response):
        temp_card = {
            "name": response["data"]["name"],
            "closed": response["data"]["closed"],
        }
    else:
        temp_card = {"name": None, "closed": None}
    return temp_card

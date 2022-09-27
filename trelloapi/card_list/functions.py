from typing import Dict, List

from ..constructors import has_card
from ..trello_requests import get_request, was_successful


def fetch_data(card_list) -> Dict[str, str]:
    """Loads CardList information."""
    url = f"https://api.trello.com/1/lists/{card_list.id}"
    response = get_request(card_list, url)
    if was_successful(response):
        temp_list = {
            "name": response["data"]["name"],
            "closed": response["data"]["closed"],
        }
    else:
        temp_list = {"name": None, "closed": None}
    return temp_list


def add_card(card_list, card: Dict[str, str]) -> List[str]:
    """Add a new Card to the List."""
    should_add = True
    if len(card_list.cards) != 0 and has_card(card_list, card["id"]):
        for stored_card in card_list.cards:
            if stored_card["id"] == card["id"]:
                should_add = False
    if should_add:
        card_list.cards.append(
            {
                "id": card["id"],
                "name": card["name"],
                "closed": card["closed"],
            }
        )
    return card_list.cards


def fetch_cards(card_list) -> Dict[str, str]:
    """Requests all Cards the current CardList has from Trello API."""
    url = f"https://api.trello.com/1/lists/{card_list.id}/cards"
    response = get_request(card_list, url)
    cards = []
    if was_successful(response):
        for card in response["data"]:
            cards = add_card(card_list, card)
    return cards

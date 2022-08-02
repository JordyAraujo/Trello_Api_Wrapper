import json
from typing import Dict, Type

from .base_class import BaseClass
from .trello_requests import get_request, was_successful


class CardList(BaseClass):
    """List class definition. It holds and interacts with the Cards."""

    def __init__(self, trello: Type[BaseClass], list_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.id = list_id
        temp_list = self.fetch_data()
        self.name = temp_list["name"]
        self.closed = temp_list["closed"]

    def fetch_data(self) -> Dict[str, str]:
        """Loads CardList information."""
        url = f"https://api.trello.com/1/lists/{self.id}"
        response = get_request(self, url)
        if was_successful(response):
            card_list = {
                "id": response["data"]["id"],
                "name": response["data"]["name"],
                "closed": response["data"]["closed"],
            }
        else:
            card_list = {"id": None, "name": None, "closed": None}
        return card_list

    def __str__(self) -> str:
        card_list = {"id": self.id, "name": self.name, "closed": self.closed}
        return json.dumps(card_list)

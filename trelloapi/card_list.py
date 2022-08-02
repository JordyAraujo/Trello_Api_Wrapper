from typing import Dict, Type

from .base_class import BaseClass
from .utils import trello_requests


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
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            card_list = {
                "id": response["data"]["id"],
                "name": response["data"]["name"],
                "closed": response["data"]["closed"],
            }
        else:
            card_list = {"id": None, "name": None, "closed": None}
        return card_list

    # def has_card(self, card_id: str) -> bool:
    #     """Check if the Card exists on the List."""
    #     url = f"https://api.trello.com/1/lists/{card_id}"
    #     response = trello_requests.get_request(self, url)
    #     return response["status"] == 200

    def __str__(self) -> str:
        """Print List by ID, Name and if it's Closed."""
        return f"{self.id} - {self.name} - {self.closed}"

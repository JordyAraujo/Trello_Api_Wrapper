from typing import Dict, Type

from .base_class import BaseClass
from .utils import trello_requests


class CardsList(BaseClass):
    """List class definition. It holds and interacts with the Cards."""

    def __init__(self, trello: Type[BaseClass], list_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.__list_id = list_id
        temp_list = self.fetch_data()
        self.__name = temp_list["name"]
        self.__closed = temp_list["closed"]

    @property
    def list_id(self) -> str:
        return self.__list_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def closed(self) -> str:
        return self.__closed

    def fetch_data(self) -> Dict[str, str]:
        """Loads CardsList information."""
        url = f"https://api.trello.com/1/lists/{self.list_id}"
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
        return f"{self.list_id} - {self.name} - {self.closed}"

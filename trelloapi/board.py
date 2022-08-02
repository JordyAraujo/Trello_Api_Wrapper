from typing import Dict, List, Type

from .base_class import BaseClass
from .card_list import CardList
from .utils import trello_requests


class Board(BaseClass):
    """Board class definition. It holds and interacts with the Lists."""

    def __init__(self, trello: Type[BaseClass], board_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.__board_id = board_id
        board = self.fetch_data()
        self.name = board["name"]
        self.closed = board["closed"]
        self.__lists = []
        self.fetch_lists()

    @property
    def board_id(self) -> str:
        return self.__board_id

    @property
    def lists(self) -> List[str]:
        return self.__lists

    def fetch_data(self) -> Dict[str, str]:
        """Loads board information."""
        url = f"https://api.trello.com/1/boards/{self.board_id}"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            board = {
                "name": response["data"]["name"],
                "closed": response["data"]["closed"],
            }
        else:
            board = {"name": None, "closed": None}
        return board

    def has_list(self, list_id: str) -> bool:
        """Check if the List exists on the Board."""
        has_it = False
        url = f"https://api.trello.com/1/lists/{list_id}"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            if response["data"]["idBoard"] == self.board_id:
                has_it = True
        return has_it

    def add_list(self, list_to_add: Dict[str, str]) -> List[str]:
        """Add a new List to the Board."""
        should_add = True
        if len(self.lists) != 0 and self.has_list(list_to_add["id"]):
            for stored_list in self.lists:
                if stored_list["id"] == list_to_add["id"]:
                    should_add = False
        if should_add:
            self.lists.append(
                {
                    "id": list_to_add["id"],
                    "name": list_to_add["name"],
                    "closed": list_to_add["closed"],
                }
            )
        return self.lists

    def fetch_lists(self) -> Dict[str, str]:
        """Requests all List the current Board has from Trello API."""
        url = f"https://api.trello.com/1/boards/{self.board_id}/lists"
        response = trello_requests.get_request(self, url)
        if response["status"] == 200:
            for trello_list in response["data"]:
                self.add_list(trello_list)
        else:
            self.__lists = []
        return {
            "status": response["status"],
            "url": url,
            "data": self.lists,
        }

    def card_list(self, list_id: str) -> Type[CardList]:
        """Get by ID a new instance of a CardList the Board has."""
        return CardList(self, list_id) if self.has_list(list_id) else None

    def __str__(self) -> str:
        """Print Board by ID, and Name."""
        return f"{self.board_id} - {self.name}"

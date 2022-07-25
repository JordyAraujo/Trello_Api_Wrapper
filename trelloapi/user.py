from typing import Dict, List, Type

from .base_class import BaseClass
from .board import Board
from .utils import trello_requests


class User(BaseClass):
    """User class definition. It holds and interacts with the Boards."""

    def __init__(self, apikey: str, token: str) -> None:
        super().__init__(apikey, token)
        self.fetch_data()
        self.__board_ids = []
        self.fetch_board_ids()

    @property
    def board_ids(self) -> List[str]:
        return self.__board_ids

    def fetch_data(self) -> Dict[str, str]:
        """Load all User data."""
        url = "https://api.trello.com/1/members/me"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            self.user = {
                "id": response["data"]["id"],
                "fullName": response["data"]["fullName"],
                "url": response["data"]["url"],
                "username": response["data"]["username"],
            }
        else:
            self.user = {
                "id": None,
                "fullName": None,
                "url": None,
                "username": None,
            }
        return self.user

    def has_board(self, board_id: str) -> bool:
        """Check if the Board exists for User."""
        url = f"https://api.trello.com/1/boards/{board_id}"
        response = trello_requests.get_request(self, url)
        return response["status"] == 200

    def add_board_id(self, board_id: str) -> List[str]:
        """Add a new Board ID to the list."""
        if self.has_board(board_id):
            if len(self.board_ids) == 0:
                self.board_ids.append(board_id)
            else:
                if board_id not in self.board_ids:
                    self.board_ids.append(board_id)
        return self.board_ids

    def fetch_board_ids(self) -> Dict[str, str]:
        """Requests all Board IDs the current User has from Trello API."""
        url = "https://api.trello.com/1/members/me/boards"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            for board in response["data"]:
                self.add_board_id(board["id"])
        else:
            self.__board_ids = []
        return {
            "status": response["status"],
            "url": url,
            "data": self.board_ids,
        }

    def board(self, board_id: str) -> Type[Board]:
        """Get by ID a new instance of a Board the User has."""
        return Board(self, board_id) if self.has_board(board_id) else None

    def __str__(self) -> str:
        """Print current User by Username and Name."""
        return f'{self.user["username"]} - {self.user["fullName"]}'

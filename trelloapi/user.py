from typing import Dict, List, Type

from .base_class import BaseClass
from .board import Board
from .utils import trello_requests


class User(BaseClass):
    """User class definition. It holds and interacts with the Boards."""

    def __init__(self, apikey: str, token: str) -> None:
        super().__init__(apikey, token)
        user = self.fetch_data()
        self.__full_name = user["full_name"]
        self.__username = user["username"]
        self.__board_ids = []
        self.fetch_board_ids()

    @property
    def full_name(self) -> str:
        return self.__full_name

    @property
    def username(self) -> str:
        return self.__username

    @property
    def board_ids(self) -> List[str]:
        self.fetch_board_ids()
        return self.__board_ids

    def fetch_data(self) -> None:
        """Load all User data."""
        self.fetch_board_ids()
        url = "https://api.trello.com/1/members/me"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            user = {
                "full_name": response["data"]["fullName"],
                "username": response["data"]["username"],
            }
        else:
            user = {"full_name": None, "username": None}
        return user

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
        return f"{self.full_name} - {self.username}"

import json
from typing import Dict, List, Type

from .base_class import BaseClass
from .board import Board
from .utils import trello_requests


class User(BaseClass):
    """User class definition. It holds and interacts with the Boards."""

    def __init__(self, apikey: str, token: str) -> None:
        super().__init__(apikey, token)
        self.__boards = []
        self.fetch_boards()
        user = self.fetch_data()
        self.id = user["id"]
        self.__full_name = user["full_name"]
        self.__username = user["username"]

    @property
    def full_name(self) -> str:
        return self.__full_name

    @property
    def username(self) -> str:
        return self.__username

    @property
    def boards(self) -> List[str]:
        return self.__boards

    def fetch_data(self) -> None:
        """Load all User data."""
        self.fetch_boards()
        url = "https://api.trello.com/1/members/me"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            user = {
                "id": response["data"]["id"],
                "full_name": response["data"]["fullName"],
                "username": response["data"]["username"],
            }
        else:
            user = {"id": None, "full_name": None, "username": None}
        return user

    def has_board(self, board_id: str) -> bool:
        """Check if the Board exists for User."""
        url = f"https://api.trello.com/1/boards/{board_id}"
        response = trello_requests.get_request(self, url)
        return response["status"] == 200

    def add_board(self, board: Dict[str, str]) -> List[str]:
        """Add a new Board to the list."""
        should_add = True
        if len(self.boards) != 0 and self.has_board(board["id"]):
            for stored_board in self.boards:
                if stored_board["id"] == board["id"]:
                    should_add = False
        if should_add:
            self.boards.append(
                {
                    "id": board["id"],
                    "name": board["name"],
                    "closed": board["closed"],
                }
            )
        return self.boards

    def fetch_boards(self) -> Dict[str, str]:
        """Requests all Board IDs the current User has from Trello API."""
        url = "https://api.trello.com/1/members/me/boards"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            for board in response["data"]:
                self.add_board(board)
        else:
            self.__boards = []
        return {
            "status": response["status"],
            "url": url,
            "data": self.boards,
        }

    def board(self, board_id: str) -> Type[Board]:
        """Get by ID a new instance of a Board the User has."""
        return Board(self, board_id) if self.has_board(board_id) else None

    def __str__(self) -> str:
        user = {
            "username": self.username,
            "full_name": self.full_name,
            "boards": self.boards,
        }
        return json.dumps(user)

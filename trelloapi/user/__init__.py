import json
from typing import List

from ..base_class import BaseClass
from .functions import fetch_boards, fetch_data


class User(BaseClass):
    """User class definition. It holds and interacts with the Boards."""

    def __init__(self, apikey: str, token: str) -> None:
        super().__init__(apikey, token)
        self.__boards = []
        self.__boards = fetch_boards(self)
        user = fetch_data(self)
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

    def __str__(self) -> str:
        user = {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "boards": self.boards,
        }
        return json.dumps(user)

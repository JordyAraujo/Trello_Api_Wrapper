import json
from typing import List, Type

from ..base_class import BaseClass
from .functions import fetch_data, fetch_lists


class Board(BaseClass):
    """Board class definition. It holds and interacts with the Lists."""

    def __init__(self, trello: Type[BaseClass], board_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.id = board_id
        self.__lists = []
        self.update()

    @property
    def lists(self) -> List[str]:
        return self.__lists

    def update(self) -> None:
        board = fetch_data(self)
        self.name = board["name"]
        self.closed = board["closed"]
        self.__lists = fetch_lists(self)

    def __str__(self) -> str:
        board = {
            "id": self.id,
            "name": self.name,
            "closed": self.closed,
            "lists": self.lists,
        }
        return json.dumps(board)

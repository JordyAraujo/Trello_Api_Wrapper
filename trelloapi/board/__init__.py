import json
from typing import List, Type

from ..base_class import BaseClass
from ..card_list import CardList
from .functions import fetch_data, fetch_lists, has_list


class Board(BaseClass):
    """Board class definition. It holds and interacts with the Lists."""

    def __init__(self, trello: Type[BaseClass], board_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.id = board_id
        board = fetch_data(self)
        self.name = board["name"]
        self.closed = board["closed"]
        self.__lists = []
        self.__lists = fetch_lists(self)

    @property
    def lists(self) -> List[str]:
        return self.__lists

    def card_list(self, list_id: str) -> Type[CardList]:
        """Get by ID a new instance of a CardList the Board has."""
        return CardList(self, list_id) if has_list(self, list_id) else None

    def __str__(self) -> str:
        board = {
            "id": self.id,
            "name": self.name,
            "closed": self.closed,
            "lists": self.lists,
        }
        return json.dumps(board)

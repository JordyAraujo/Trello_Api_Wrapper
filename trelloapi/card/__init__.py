from typing import Type

from ..base_class import BaseClass
from .functions import fetch_data


class Card(BaseClass):
    """Card class definition. Those are the main components of the project."""

    def __init__(self, trello: Type[BaseClass], card_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.id = card_id
        self.update()

    def update(self) -> None:
        card = fetch_data(self)
        self.name = card["name"]
        self.closed = card["closed"]

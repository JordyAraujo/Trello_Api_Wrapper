import json
from typing import List, Type

from ..base_class import BaseClass
from .functions import fetch_cards, fetch_data

# from ..card import Card


class CardList(BaseClass):
    """List class definition. It holds and interacts with the Cards."""

    def __init__(self, trello: Type[BaseClass], list_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.id = list_id
        temp_list = fetch_data(self)
        self.name = temp_list["name"]
        self.closed = temp_list["closed"]
        self.__cards = []
        self.__cards = fetch_cards(self)

    @property
    def cards(self) -> List[str]:
        return self.__cards

    # def card(self, card_id: str) -> Type[Card]:
    #     """Get by ID a new instance of a Card the CardList has."""
    #     return Card(self, card_id) if has_card(self, card_id) else None

    def __str__(self) -> str:
        card_list = {
            "id": self.id,
            "name": self.name,
            "closed": self.closed,
            "cards": self.cards,
        }
        return json.dumps(card_list)

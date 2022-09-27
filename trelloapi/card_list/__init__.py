import json
from typing import List, Type

import requests

from ..base_class import BaseClass
from .functions import fetch_cards, fetch_data

CREATE_CARD_URL = "https://api.trello.com/1/cards"


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

    def create_card(self, title, description, label_ids):
        """Create a new Trello card"""
        params = {
            "name": title,
            "desc": description,
            "pos": "top",
            "idList": self.id,
            "key": super().apikey,
            "token": super().token,
            "idLabels": label_ids,
        }
        response = requests.request("POST", CREATE_CARD_URL, params=params)
        card_id = response.json()["id"] if response.ok else None
        return card_id, response.status_code

    def __str__(self) -> str:
        card_list = {
            "id": self.id,
            "name": self.name,
            "closed": self.closed,
            "cards": self.cards,
        }
        return json.dumps(card_list)

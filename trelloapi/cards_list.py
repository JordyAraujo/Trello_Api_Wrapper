"""List class definition. It holds and interacts with the Cards."""
from .base_class import BaseClass
from .utils import trello_requests


class CardsList(BaseClass):
    """List class definition. It holds and interacts with the Cards."""

    def __init__(self, trello, list_id):
        """Class constructor."""
        super().__init__(trello.apikey, trello.token)
        self.__list_id = list_id
        temp_list = self.auto_load()
        self.__name = temp_list["name"]
        self.__closed = temp_list["closed"]

    @property
    def list_id(self):
        """Getter for __list_id"""
        return self.__list_id

    @property
    def name(self):
        """Getter for __name"""
        return self.__name

    @property
    def closed(self):
        """Getter for __closed"""
        return self.__closed

    def auto_load(self):
        """Loads list information."""
        url = f"https://api.trello.com/1/lists/{self.list_id}"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            card_list = {
                "id": response["data"]["id"],
                "name": response["data"]["name"],
                "closed": response["data"]["closed"],
            }
        else:
            card_list = {"id": None, "name": None, "closed": None}
        return card_list

    # def has_card(self, card_id):
    #     """Check if the Card exists on the List."""
    #     url = f"https://api.trello.com/1/lists/{card_id}"
    #     response = trello_requests.get_request(self, url)
    #     return response["status"] == 200

    def __str__(self):
        """Print List by ID and name."""
        return f"{self.list_id} - {self.name}"

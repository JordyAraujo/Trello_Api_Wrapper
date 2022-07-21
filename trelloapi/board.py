"""Board class definition. It holds and interacts with the Lists."""
from .base_class import BaseClass
from .cards_list import CardsList
from .utils import trello_requests


class Board(BaseClass):
    """Board class definition. It holds and interacts with the Lists."""

    def __init__(self, trello, board_id):
        """Class constructor."""
        super().__init__(trello.apikey, trello.token)
        self.__board_id = board_id
        board = self.auto_load()
        self.__name = board["name"]
        self.__url = board["url"]
        self.__list_ids = []
        self.fetch_list_ids()

    @property
    def board_id(self):
        """Getter for __board_id"""
        return self.__board_id

    @property
    def name(self):
        """Getter for __name"""
        return self.__name

    @property
    def url(self):
        """Getter for __url"""
        return self.__url

    @property
    def list_ids(self):
        """Getter for __list_ids"""
        return self.__list_ids

    def auto_load(self):
        """Loads board information."""
        url = f"https://api.trello.com/1/boards/{self.board_id}"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            board = {
                "id": response["data"]["id"],
                "name": response["data"]["name"],
                "url": response["data"]["url"],
            }
        else:
            board = {"id": None, "name": None, "url": None}
        return board

    def has_list(self, list_id):
        """Check if the List exists on the Board."""
        has_it = False
        url = f"https://api.trello.com/1/lists/{list_id}"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            if response["data"]["idBoard"] == self.board_id:
                has_it = True
        return has_it

    def add_list_id(self, list_id):
        """Add a new List ID to the list."""
        if self.has_list(list_id):
            if len(self.list_ids) == 0:
                self.list_ids.append(list_id)
            else:
                if list_id not in self.list_ids:
                    self.list_ids.append(list_id)
        return self.list_ids

    def fetch_list_ids(self):
        """Requests all List IDs the current Board has from Trello API."""
        url = f"https://api.trello.com/1/boards/{self.board_id}/lists"
        response = trello_requests.get_request(self, url)
        if response["status"] == 200:
            for trello_list in response["data"]:
                self.add_list_id(trello_list["id"])
        else:
            self.__list_ids = []
        return {
            "status": response["status"],
            "url": url,
            "data": self.list_ids,
        }

    def cards_list(self, list_id):
        """Get by ID a new instance of a CardsList the Board has."""
        return CardsList(self, list_id) if self.has_list(list_id) else None

    def __str__(self):
        """Print Board by name."""
        return f"{self.board_id} - {self.name} - {self.url}"

"""Board class definition. It holds and interacts with the Lists."""
from .utils import trello_requests


class Board:
    """Board class definition. It holds and interacts with the Lists."""

    def __init__(self, trello, board_id):
        """Class constructor."""
        self.apikey = trello.apikey
        self.token = trello.token
        self.board_id = board_id
        board = self.auto_load()
        self.name = board["name"]
        self.url = board["url"]
        self.list_ids = []
        self.fetch_list_ids()

    def auto_load(self):
        """Loads board information."""
        url = f"https://api.trello.com/1/boards/{self.board_id}"
        response = trello_requests.get_request(self, url)
        if len(response) != 0 and response["status"] == 200:
            board = {
                "id": response["data"]["id"],
                "name": response["data"]["name"],
                "url": response["data"]["url"],
            }
        else:
            board = {"id": None, "name": None, "url": None}
        return board

    def has_list(self, list_id):
        """Check if the List exists for Board."""
        url = f"https://api.trello.com/1/lists/{list_id}"
        response = trello_requests.get_request(self, url)
        return response["status"] == 200

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
            self.list_ids = []
        return {
            "status": response["status"],
            "url": url,
            "data": self.list_ids,
        }

    def __str__(self):
        """Print Board by name."""
        return f"{self.board_id} - {self.name} - {self.url}"

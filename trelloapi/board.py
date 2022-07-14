"""Board class definition. It holds and interacts with the Cards."""
from .apibase import ApiBase
from .utils import trello_requests


class Board(ApiBase):
    """Board class definition. It holds and interacts with the Cards."""

    def __init__(self, trello, board_id):
        """Class constructor."""
        self._apikey = trello.apikey()
        self._token = trello.token()
        self.board_id = board_id
        self.cards_list = []
        board = self.auto_load()
        self.name = board["name"]
        self.url = board["url"]

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

    def __str__(self):
        """Print Board by name."""
        return f"{self.board_id} - {self.name}"

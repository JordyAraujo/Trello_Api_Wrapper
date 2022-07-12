"""Board class definition. It holds and interacts with the Cards."""


class Board:
    """Board class definition. It holds and interacts with the Cards."""

    def __init__(self, board_id):
        """Class constructor."""
        self.board_id = board_id

    def list_cards(self):
        """Requests all Cards this Board has from Trello API."""

    def set_cards(self):
        """Set an updated list of Cards for this Board."""

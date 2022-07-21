"""Lib initializer."""
from .user import User


class Trello(User):
    """Lib initializer."""

    def trello_user(self):
        """Get a new instance of the Trello User."""
        return User(self.apikey, self.token)

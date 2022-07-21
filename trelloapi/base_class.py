"""Base Class for all trello based objects."""


class BaseClass:
    """Base Class for all trello based objects."""

    def __init__(self, apikey, token):
        """Class constructor."""
        self.__apikey = apikey
        self.__token = token

    @property
    def apikey(self):
        """Getter for __apikey"""
        return self.__apikey

    @property
    def token(self):
        """Getter for __token"""
        return self.__token

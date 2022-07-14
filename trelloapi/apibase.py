"""Base Class for the library."""


class ApiBase:
    """Base Class for the library."""

    _apikey = None
    _token = None

    def apikey(self):
        """Getter for apikey."""
        return self._apikey

    def token(self):
        """Getter for token."""
        return self._token

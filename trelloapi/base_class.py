"""Base Class for all trello based objects."""


class BaseClass:
    def __init__(self, apikey: str, token: str) -> None:
        self.__apikey = apikey
        self.__token = token

    @property
    def apikey(self) -> str:
        return self.__apikey

    @property
    def token(self) -> str:
        return self.__token

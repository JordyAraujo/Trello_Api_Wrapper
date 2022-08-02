"""Base Class for all trello based objects."""


class BaseClass:
    def __init__(self, apikey: str, token: str) -> None:
        self.__apikey = apikey
        self.__token = token
        self.__name = "BaseClass"
        self.__closed = False

    @property
    def apikey(self) -> str:
        return self.__apikey

    @property
    def token(self) -> str:
        return self.__token

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        self.__name = new_name

    @property
    def closed(self) -> bool:
        return self.__closed

    @closed.setter
    def closed(self, new_closed: bool) -> None:
        self.__closed = new_closed

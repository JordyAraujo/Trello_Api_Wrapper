from typing import Type

from .user import User


class Trello(User):
    def user(self) -> Type[User]:
        """Instantiate a new Trello User."""
        return User(self.apikey, self.token)

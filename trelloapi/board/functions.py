from typing import Dict, List

from ..trello_requests import get_request, was_successful


def fetch_data(board) -> Dict[str, str]:
    """Loads Board information."""
    url = f"https://api.trello.com/1/boards/{board.id}"
    response = get_request(board, url)
    if was_successful(response):
        board = {
            "name": response["data"]["name"],
            "closed": response["data"]["closed"],
        }
    else:
        board = {"name": None, "closed": None}
    return board


def has_list(board, list_id: str) -> bool:
    """Check if the List exists on the Board."""
    has_it = False
    url = f"https://api.trello.com/1/lists/{list_id}"
    response = get_request(board, url)
    if was_successful(response):
        if response["data"]["idBoard"] == board.id:
            has_it = True
    return has_it


def add_list(board, list_to_add: Dict[str, str]) -> List[str]:
    """Add a new List to the Board."""
    should_add = True
    if len(board.lists) != 0 and has_list(board, list_to_add["id"]):
        for stored_list in board.lists:
            if stored_list["id"] == list_to_add["id"]:
                should_add = False
    if should_add:
        board.lists.append(
            {
                "id": list_to_add["id"],
                "name": list_to_add["name"],
                "closed": list_to_add["closed"],
            }
        )
    return board.lists


def fetch_lists(board) -> Dict[str, str]:
    """Requests all List the current Board has from Trello API."""
    url = f"https://api.trello.com/1/boards/{board.id}/lists"
    response = get_request(board, url)
    lists = []
    if was_successful(response):
        for trello_list in response["data"]:
            lists = add_list(board, trello_list)
    return lists

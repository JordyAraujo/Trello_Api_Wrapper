import httpx

class Trello:
    def __init__(self, apikey, token):
        self._apikey = apikey
        self._token = token

        boards = self.list_boards()

        if boards["status"] == 200:
            self.board_list = boards["boards"]
        else:
            self.board_list = None


    def list_boards(self):
        try:
            url = "https://api.trello.com/1/members/me/boards"

            headers = {
                "Accept": "application/json"
            }

            params = {
                'key': self._apikey,
                'token': self._token
            }

            response = httpx.get(url, headers=headers, params=params)
            response.raise_for_status()
            return({
                "status": response.status_code,
                "boards": [{
                    "id": board["id"],
                    "name": board["name"],
                    } for board in response.json()
                ]
            })
        except httpx.HTTPStatusError as exc:
            return({
                "status": exc.response.status_code,
                "url": f"{exc.request.url}"
            })

"""Useful request shortcuts."""
import httpx


def get_request(
    trello,
    url,
    data=None,
):
    """Get request with a scent of Trello."""
    data = data or {}
    try:
        headers = {"Accept": "application/json"}
        param = {"key": trello.apikey(), "token": trello.token()}
        response = httpx.get(url, headers=headers, params={**param, **data})
        response.raise_for_status()
        return {
            "status": response.status_code,
            "url": url,
            "data": response.json(),
        }
    except httpx.HTTPStatusError as exc:
        return {"status": exc.response.status_code, "url": url, "data": []}

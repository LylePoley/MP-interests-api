from httpx import Response, Client
from typing import Any, Mapping


class httpxResponseAdapter:
    def __init__(self, response: Response):
        self.response = response

    def json(self) -> Any:
        return self.response.json()

    def raise_for_status(self) -> None:
        self.response.raise_for_status()

    @property
    def status_code(self) -> int:
        return self.response.status_code


class httpxClientAdapter:
    def __init__(self, client: Client):
        self.client = client

    def get(
        self, url: str, *, params: Mapping[str, Any] | None = None
    ) -> httpxResponseAdapter:
        return httpxResponseAdapter(self.client.get(url, params=params))


member_client = httpxClientAdapter(
    Client(base_url="https://members-api.parliament.uk/api", follow_redirects=True)
)
interest_client = httpxClientAdapter(
    Client(base_url="https://interests-api.parliament.uk/api/v1", follow_redirects=True)
)

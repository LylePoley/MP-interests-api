from typing import Any, Mapping
import json
import os


class MockResponse:
    def __init__(self, data_location: str):
        self.data_location = data_location

    def json(self) -> Any:
        with open(self.data_location, "r") as f:
            return json.load(f)

    def raise_for_status(self) -> None: ...

    @property
    def status_code(self) -> int:
        return 200


class MockClient:
    def __init__(self, data_location: str):
        self.data_location = data_location

    def get(self, url: str, *, params: Mapping[str, Any] | None = None) -> MockResponse:
        return MockResponse(self.data_location)


mock_member_client = MockClient(
    os.getcwd() + "/backend/client/mock_responses/mock_member_response.json"
)
mock_interest_client = MockClient(
    os.getcwd() + "/backend/client/mock_responses/mock_interest_response.json"
)

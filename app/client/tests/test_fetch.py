import json
from unittest.mock import Mock
from pathlib import Path
from typing import Dict, Any
import pytest
from functools import partial

from app.client import Client, Response
from app.client.fetch import fetch_all


members_data = json.loads(
    Path("app/client/mock_responses/mock_member_response.json").read_text()
)
interests_data = json.loads(
    Path("app/client/mock_responses/mock_interest_response.json").read_text()
)


def mock_get(
    mock_data: Dict[str, Any], url: str, params: Dict[str, Any] | None = None
) -> Response:
    skip = params.get("skip", 0) if params else 0
    take = params.get("take", 20) if params else 20

    response = Mock(spec=Response)
    response.status_code = 200
    response.raise_for_status.return_value = None
    mock_response_data: Dict[str, Any] = {}
    mock_response_data["items"] = mock_data["items"][skip : skip + take]
    response.json.return_value = mock_response_data

    return response


@pytest.mark.parametrize(
    "mock_data, relative_url, params",
    [
        (members_data, "/Members/Search", {"IsCurrentMember": "true", "take": 20}),
        (interests_data, "/Interests", {"ExpandChildInterests": "false"}),
    ],
)
def test_fetch_all(
    mock_data: Dict[str, Any], relative_url: str, params: Dict[str, Any]
):
    mock_client = Mock(spec=Client)
    mock_client.get.side_effect = partial(mock_get, mock_data)

    results = list(fetch_all(mock_client, relative_url, params))

    assert results == mock_data["items"]

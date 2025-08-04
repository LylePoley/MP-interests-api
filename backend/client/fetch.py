from backend.client import Client, Response

from typing import Any, Iterable, Dict
from logging import getLogger, Logger

logger = getLogger(__name__)

def fetch_all(
        client: Client,
        relative_url: str,
        params: Dict[str, Any],
        description: str | None = None,
        logger: Logger | None = None
    ) -> Iterable[Dict[str, Any]]:
    if logger:
        logger.info(f"Fetching {description or 'items'} from {relative_url} with params: {params}")

    skip: int = 0

    while True:
        response = client.get(relative_url, params={**params, "skip": skip})

        response.raise_for_status()

        data = response.json()

        skip += len(data.get("items", []))

        for item in data.get("items", []):
            yield item

        if len(data.get("items", [])) < 20:
            if logger:
                logger.info(f"Fetched {skip} items in total.")
            break

    return


def fetch_all_active_members(client: Client) -> Iterable[Dict[str, Any]]:
    return fetch_all(
        client=client,
        relative_url="/Members/Search",
        params={"IsCurrentMember": "true", "take": 20},
        description="active members",
        logger=logger,
    )

def fetch_all_interest_categories(client: Client) -> Iterable[Dict[str, Any]]:
    return fetch_all(
        client=client,
        relative_url="/Categories",
        params={},
        description="interest categories",
        logger=logger,
    )

def fetch_all_interests(client: Client) -> Iterable[Dict[str, Any]]:
    return fetch_all(
        client=client,
        relative_url="/Interests",
        params={"ExpandChildInterests": "false"},
        description="interests",
        logger=logger,
    )
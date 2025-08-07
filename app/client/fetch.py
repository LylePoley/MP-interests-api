from app.client import Client

from typing import Any, Iterable, Dict
from logging import Logger


def fetch_all(
    client: Client,
    relative_url: str,
    params: Dict[str, Any],
    description: str | None = None,
    logger: Logger | None = None,
) -> Iterable[Dict[str, Any]]:
    """
    Fetch all items from a paginated API endpoint. Goes through the pages of the API response until all items are fetched.
    """
    if logger:
        logger.info(
            f"Fetching {description or 'items'} from {relative_url} with params: {params}"
        )

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


def fetch_all_active_members(
    client: Client, logger: Logger | None = None
) -> Iterable[Dict[str, Any]]:
    return fetch_all(
        client=client,
        relative_url="/Members/Search",
        params={"IsCurrentMember": "true", "take": 20},
        description="active members",
        logger=logger,
    )


def fetch_all_interests(
    client: Client, logger: Logger | None = None
) -> Iterable[Dict[str, Any]]:
    return fetch_all(
        client=client,
        relative_url="/Interests",
        params={"ExpandChildInterests": "false"},
        description="interests",
        logger=logger,
    )

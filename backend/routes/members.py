from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from typing import List, Annotated

from backend.models import Member
from backend.core.db import get_session
import backend.core.filters as filter
from datetime import datetime

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/search", response_model=List[Member], operation_id="search_members")
def search_members(*, session: Session = Depends(get_session),
    name: Annotated[str | None,
                    Query(description="Name of the member to search for. Supports partial matches and is case insensitive.",
                          example="kier")]=None,
    party: Annotated[str | None,
                    Query(description="Name of the party to filter members by, supports partial matches and is case insensitive.",
                          example="lab")]=None,
    house: Annotated[int | None,
                    Query(description="House ID members by. 1 for Commons, 2 for Lords")]=None,
    membership_started_since: Annotated[datetime | None,
                    Query(description="Filter by members whose membership started since this date in ISO format (YYYY-MM-DD).",
                          example="2012-12-25")]=None,
    membership_ended_since: Annotated[datetime | None,
                    Query(description="Filter by members whose membership ended since this date in ISO format (YYYY-MM-DD).")]=None,
    skip: Annotated[int,
                    Query(description="Number of records to skip for pagination. E.g. 50 will skip the first 50 records")]=0,
    take: Annotated[int | None,
                    Query(description="Number of records to return. E.g. 20 will return the next 20 records after the skipped ones")]=None,
) -> List[Member]:
    """
    Search members matching the given criteria.

    Arguments:
    - name: Name of the member to search for. Supports partial matches and is case insensitive e.g. 'John' and 'sm' will match 'John Smith'
    - party: Name of the party to filter members by. Supports partial matches and is case insensitive.
    - house: House ID to filter members by. 1 for Commons, 2 for Lords.
    - membership_started_since: Filter by members whose membership started since this date. Supports ISO format (YYYY-MM-DD).
    - membership_ended_since: Filter by members whose membership ended since this date. Supports ISO format (YYYY-MM-DD).
    - skip: Number of records to skip for pagination. E.g. 50 will skip the first 50 records.
    - take: Number of records to return. E.g. 20 will return the next 20 records after the skipped ones.

    Returns:

    members: List[Member]

    List of the details of each member matching the criteria.

    Examples:
    Get first two members in the database who have started since 2025 from the Labour party:
    - `HOST/members/search?party=lab&embership_started_since=2025&take=2`
    ```json
    [
        {
            "name_list_as":"May of Maidenhead, B.",
            "name_display_as":"Baroness May of Maidenhead",
            "name_address_as":null,
            "thumbnail_url":"https://members-api.parliament.uk/api/Members/8/Thumbnail",
            "house":2,
            "membership_from_id":4,
            "membership_end_date":null,
            "status_is_active":true,
            "id":8,
            "name_full_title":"The Rt Hon. the Baroness May of Maidenhead",
            "gender":"F",
            "party_id":4,
            "membership_from":"Life peer",
            "membership_start_date":"2024-08-21T00:00:00",
            "membership_end_reason":null,
            "status_start_date":"2024-08-21T00:00:00"
        },
        {
            "name_list_as":"Pickles, L.",
            "name_display_as":"Lord Pickles",
            "name_address_as":null,
            "thumbnail_url":"https://members-api.parliament.uk/api/Members/33/Thumbnail",
            "house":2,
            "membership_from_id":4,
            "membership_end_date":null,
            "status_is_active":true,
            "id":33,
            "name_full_title":"The Rt Hon. the Lord Pickles",
            "gender":"M",
            "party_id":4,
            "membership_from":"Life peer",
            "membership_start_date":"2018-06-18T00:00:00",
            "membership_end_reason":null,
            "status_start_date":"2018-06-18T00:00:00"
        }
    ]
    ```
    """
    statement = select(Member)
    statement = filter.by_member_name(statement, name)
    statement = filter.by_party(statement, party)
    statement = filter.by_house(statement, house)
    statement = filter.by_membership_start(statement, membership_started_since)
    statement = filter.by_membership_end(statement, membership_ended_since)

    statement = statement.offset(skip).limit(take)

    return list(session.exec(statement).all())



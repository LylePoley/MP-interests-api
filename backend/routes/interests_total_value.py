from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select, col, func
from typing import List, Annotated

from backend.models import Interest, Member, MonetaryValueField
from backend.core.db import get_session
import backend.core.filters as filter
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/interests", tags=["interests"])

class MemberWithTotalInterestValue(BaseModel):
    member: Member
    total_interests_value: float


@router.get("/search", response_model=List[MemberWithTotalInterestValue], operation_id="search_members_with_grouped_interest_values")
def search_members_with_grouped_interest_values(
    *,
    session: Session = Depends(get_session),
    member_name: Annotated[str | None, Query(description="Name of the member to search for. Supports partial matches and is case insensitive e.g. 'John' and 'sm' will match 'John Smith'")] = None,
    party: Annotated[str | None, Query(description="Name of the party to filter members by, supports partial matches and is case insensitive.")] = None,
    house: Annotated[int | None, Query(description="House ID to filter members by. 1 for Commons, 2 for Lords")] = None,
    published_before: Annotated[datetime | None, Query(description="Filter by interests published before this date in ISO format (YYYY-MM-DD).")] = None,
    published_after: Annotated[datetime | None, Query(description="Filter by interests published after this date in ISO format (YYYY-MM-DD).")] = None,
    skip: Annotated[int, Query(description="Number of records to skip for pagination. E.g. 50 will skip the first 50 records")] = 0,
    take: Annotated[int | None, Query(description="Number of records to return. E.g. 20 will return the next 20 records after the skipped ones")] = None,
) -> List[MemberWithTotalInterestValue]:
    """
    Search members and when their interests where published. Results are returned sorted in descending value of interests.

    Arguments:

    - member_name: Name of the member to search for. Supports partial matches and is case insensitive e.g. 'John' and 'sm' will match 'John Smith'
    - party: Name of the party to filter members by. Supports partial matches and is case insensitive.
    - house: House ID to filter members by. 1 for Commons, 2 for Lords.
    - published_before: Filter by interests published before this date. Supports ISO format (YYYY-MM-DD).
    - published_after: Filter by interests published after this date. Supports ISO format (YYYY-MM-DD).
    - skip: Number of records to skip for pagination. E.g. 50 will skip the first 50 records.
    - take: Number of records to return. E.g. 20 will return the next 20 records after the skipped ones. If absent, all matching records will be returned.

    Returns:

    members: List[MemberWithTotalInterestValue]

    A list elements of type `MemberWithTotalInterestValue`, which contains a .member and a .total_interests_value field.
    Returns all members matching the search criteria, along with the total value of their interests.

    Examples:
    Get the total value of interests published in 2024 or after for members whose name contains 'diane':
    - `HOST/interests/search?name=diane&take=1&published_after=2024`
    ```json
    [
        {
            "member": {
                "name_display_as": "Ms Diane Abbott",
                "name_list_as": "Abbott, Ms Diane",
                "name_address_as": "Ms Abbott",
                "thumbnail_url": "https://members-api.parliament.uk/api/Members/172/Thumbnail",
                "house": 1,
                "membership_from_id": 4074,
                "membership_end_date": null,
                "status_is_active": true,
                "id": 172,
                "name_full_title": "Rt Hon Diane Abbott MP",
                "gender": "F",
                "party_id": 8,
                "membership_from": "Hackney North and Stoke Newington",
                "membership_start_date": "1987-06-11T00:00:00",
                "membership_end_reason": null,
                "status_start_date": "2024-07-04T00:00:00"
            },
            "total_interests_value": 29090.0
        }
    ]
    ```
    """

    statement = (
        select(Member, func.coalesce(func.sum(MonetaryValueField.value), 0).label("total"))
        .join(Interest, col(Interest.member_id) == col(Member.id), isouter=True)
        .join(MonetaryValueField, col(MonetaryValueField.interest_id) == col(Interest.id), isouter=True)
        .order_by(col("total").desc())
    )

    statement = filter.by_member_name(statement, name=member_name)
    statement = filter.by_party(statement, party)
    statement = filter.by_house(statement, house)
    statement = filter.by_interest_published_after(statement, published_after)
    statement = filter.by_interest_published_before(statement, published_before)

    statement = statement.offset(skip)

    if take:
        statement = statement.limit(take)

    statement = statement.group_by(col(Member.id))

    results = session.exec(statement).all()

    return [
        MemberWithTotalInterestValue(member=row[0], total_interests_value=row[1] if row[1] else 0.0) for row in results
    ]

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


@router.get("/search", response_model=List[MemberWithTotalInterestValue], operation_id="search_members_with_grouped_interest_values",
            description="Search members and when their interests where published. Results are returned sorted in descending value of interests.")
def search_members_with_grouped_interest_values(
    *,
    session: Session = Depends(get_session),
    member_name: Annotated[str | None, Query(description="Name of the member to search for. Supports partial matches and is case insensitive e.g. 'John' and 'sm' will match 'John Smith'")] = None,
    party: Annotated[str | None, Query(description="Name of the party to filter members by, supports partial matches and is case insensitive.")] = None,
    house: Annotated[str | int | None, Query(description="House ID to filter members by. 1 for Commons, 2 for Lords")] = None,
    published_before: Annotated[datetime | None, Query(description="Filter by interests published before this date in ISO format (YYYY-MM-DD).")] = None,
    published_after: Annotated[datetime | None, Query(description="Filter by interests published after this date in ISO format (YYYY-MM-DD).")] = None,
    skip: Annotated[str | int, Query(description="Number of records to skip for pagination. E.g. 50 will skip the first 50 records")] = 0,
    take: Annotated[str | int | None, Query(description="Number of records to return. E.g. 20 will return the next 20 records after the skipped ones")] = None,
) -> List[MemberWithTotalInterestValue]:

    # these are necessary for claude to be able to call the api
    house = int(house) if house else None
    skip = int(skip) if skip else 0
    take = int(take) if take else 20

    total = func.coalesce(func.sum(MonetaryValueField.value), 0).label("total")
    statement = (
        select(Member, total)
        .join(Interest, col(Interest.member_id) == col(Member.id), isouter=True)
        .join(MonetaryValueField, col(MonetaryValueField.interest_id) == col(Interest.id), isouter=True)
        .order_by(total.desc())
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

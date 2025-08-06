from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select, col, func
from typing import List

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
    member_name: str | None = Query(None),
    party: str | None = Query(None),
    house: int | None = Query(None),
    published_before: datetime | None = Query(None),
    published_after: datetime | None = Query(None),
    skip: int = Query(0),
    take: int = Query(20),
) -> List[MemberWithTotalInterestValue]:
    """
    Get members with optional filters and total of their interest values.
    """

    statement = (
        select(Member, func.coalesce(func.sum(MonetaryValueField.value), 0).label("total"))
        .join(Interest, col(Interest.member_id) == col(Member.id), isouter=True)
        .join(MonetaryValueField, col(MonetaryValueField.interest_id) == col(Interest.id), isouter=True)
    )

    statement = filter.by_member_name(statement, name=member_name)
    statement = filter.by_party(statement, party)
    statement = filter.by_house(statement, house)
    statement = filter.by_interest_published_after(statement, published_after)
    statement = filter.by_interest_published_before(statement, published_before)

    statement = statement.offset(skip).limit(take)
    statement = statement.group_by(col(Member.id))

    results = session.exec(statement).all()

    return [
        MemberWithTotalInterestValue(member=row[0], total_interests_value=row[1] if row[1] else 0.0) for row in results
    ]



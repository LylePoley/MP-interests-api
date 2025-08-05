from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select, col, func
from typing import List

from backend.models import Member
from backend.core.db import get_session
import backend.core.filters as filter
from datetime import datetime

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/search", response_model=List[Member])
def search_members(*, session: Session = Depends(get_session),
    name: str | None = Query(None),
    party: str | None = Query(None),
    house: int | None = Query(None),
    membership_started_since: datetime | None = Query(None),
    membership_ended_since: datetime | None = Query(None),
    skip: int = Query(0),
    take: int = Query(20),
) -> List[Member]:
    """Get members with multiple optional filters."""
    statement = select(Member)
    statement = filter.by_member_name(statement, name)
    statement = filter.by_party(statement, party)
    statement = filter.by_house(statement, house)
    statement = filter.by_membership_start_date(statement, membership_started_since)
    statement = filter.by_membership_end_date(statement, membership_ended_since)

    statement = statement.offset(skip).limit(take)

    return list(session.exec(statement).all())



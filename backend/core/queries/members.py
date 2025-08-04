from sqlmodel import Session, select, func, col
from datetime import datetime
from typing import List
from backend.models import Member, Party

def search_members(
    engine,
    name: str | None = None,
    party: str | None = None,
    house: int | None = None,
    membership_started_since: datetime | None = None,
    membership_ended_since: datetime | None = None,
    skip: int = 0,
    take: int = 20,
) -> List[Member]:
    """Get members with multiple optional filters."""
    with Session(engine) as session:
        statement = select(Member).join(Party)

        if name:
            statement = statement.where(func.lower(Member.name_display_as).like(f"%{name.lower()}%"))
        if party:
            statement = statement.where(func.lower(Party.name).like(f"%{party.lower()}%"))
        if house:
            statement = statement.where(Member.house == house)
        if membership_started_since:
            statement = statement.where(col(Member.membership_start_date) >= membership_started_since)
        if membership_ended_since:
            statement = statement.where(col(Member.membership_end_date) <= membership_ended_since)

        statement = statement.offset(skip)
        statement = statement.limit(take)
        results = session.exec(statement)

        return list(results)
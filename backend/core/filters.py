from sqlmodel import func, col

from datetime import datetime
from backend.models import Member, Party, Interest
from datetime import date

def by_member_name(statement, name: str | None):
    if name:
        return statement.where(func.lower(Member.name_display_as).like(f"%{name.lower()}%"))
    return statement

def by_party(statement, party: str | None):
    if party:
        return statement.where(func.lower(Party.name).like(f"%{party.lower()}%"))
    return statement

def by_house(statement, house: int | None):
    if house:
        return statement.where(Member.house == house)
    return statement

def by_membership_start_date(statement, membership_started_since: datetime | None):
    if membership_started_since:
        return statement.where(col(Member.membership_start_date) >= membership_started_since)
    return statement

def by_membership_end_date(statement, membership_ended_since: datetime | None):
    if membership_ended_since:
        return statement.where(col(Member.membership_end_date) <= membership_ended_since)
    return statement

def by_interest_published_date_after(statement, published_after: str | None):
    if published_after:
        return statement.where(col(Interest.published_date) >= date.fromisoformat(published_after))
    return statement

def by_interest_published_date_before(statement, published_before: str | None):
    if published_before:
        return statement.where(col(Interest.published_date) <= date.fromisoformat(published_before))
    return statement


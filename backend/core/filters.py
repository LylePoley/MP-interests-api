from backend.models import Member, Party, Interest

from sqlmodel import func, col
from typing import Optional, Any
from sqlmodel.sql.expression import Select, SelectOfScalar
from datetime import datetime


def by_member_id(
    statement: Select[Any] | SelectOfScalar[Any], member_id: Optional[int]
) -> Select[Any] | SelectOfScalar[Any]:
    if member_id:
        return statement.where(Member.id == member_id)
    return statement


def by_member_name(
    statement: Select[Any] | SelectOfScalar[Any], name: Optional[str]
) -> Select[Any] | SelectOfScalar[Any]:
    if name:
        return statement.where(
            func.lower(Member.name_display_as).like(f"%{name.lower()}%")
        )
    return statement


def by_party(
    statement: Select[Any] | SelectOfScalar[Any], party: Optional[str]
) -> Select[Any] | SelectOfScalar[Any]:
    if party:
        return statement.where(func.lower(Party.name).like(f"%{party.lower()}%"))
    return statement


def by_house(
    statement: Select[Any] | SelectOfScalar[Any], house: Optional[int]
) -> Select[Any] | SelectOfScalar[Any]:
    if house:
        return statement.where(Member.house == house)
    return statement


def by_membership_start(
    statement: Select[Any] | SelectOfScalar[Any],
    membership_started_since: Optional[datetime],
) -> Select[Any] | SelectOfScalar[Any]:
    if membership_started_since:
        return statement.where(
            col(Member.membership_start_date) >= membership_started_since
        )
    return statement


def by_membership_end(
    statement: Select[Any] | SelectOfScalar[Any],
    membership_ended_since: Optional[datetime],
) -> Select[Any] | SelectOfScalar[Any]:
    if membership_ended_since:
        return statement.where(
            col(Member.membership_end_date) <= membership_ended_since
        )
    return statement


def by_interest_published_after(
    statement: Select[Any] | SelectOfScalar[Any], published_after: Optional[datetime]
) -> Select[Any] | SelectOfScalar[Any]:
    if published_after:
        return statement.where(col(Interest.published_date) >= published_after)
    return statement


def by_interest_published_before(
    statement: Select[Any] | SelectOfScalar[Any], published_before: Optional[datetime]
) -> Select[Any] | SelectOfScalar[Any]:
    if published_before:
        return statement.where(col(Interest.published_date) <= published_before)
    return statement

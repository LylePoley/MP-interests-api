from fastapi import APIRouter, Query
from typing import List

from backend.models import Member
from backend.core import engine
from backend.core.queries import search_members as db_search_members
from datetime import datetime

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/search", response_model=List[Member])
def search_members(
    name: str | None = Query(None),
    party: str | None = Query(None),
    house: int | None = Query(None),
    membership_started_since: datetime | None = Query(None),
    membership_ended_since: datetime | None = Query(None),
    skip: int = Query(0),
    take: int = Query(20),
) -> List[Member]:
    """Get members with multiple optional filters."""
    return db_search_members(
        engine,
        name=name,
        party=party,
        house=house,
        membership_started_since=membership_started_since,
        membership_ended_since=membership_ended_since,
        skip=skip,
        take=take
    )

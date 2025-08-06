from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from typing import List, Annotated

from backend.models import Member, Party
from backend.core.db import get_session
import backend.core.filters as filter
from datetime import datetime

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/search", response_model=List[Member], operation_id="search_members",
            description="Search members by name, party, house, and membership dates.")
def search_members(*, session: Session = Depends(get_session),
    name: Annotated[str | None,
                    Query(description="Name of the member to search for. Supports partial matches and is case insensitive.",
                          example="keir")]=None,
    party: Annotated[str | None,
                    Query(description="Name of the party to filter members by, supports partial matches and is case insensitive.",
                          example="lab")]=None,
    house: Annotated[str | int | None,
                    Query(description="House ID members by. 1 for Commons, 2 for Lords")]=None,
    membership_started_since: Annotated[datetime | None,
                    Query(description="Filter by members whose membership started since this date in ISO format (YYYY-MM-DD).",
                          example="2012-12-25")]=None,
    membership_ended_since: Annotated[datetime | None,
                    Query(description="Filter by members whose membership ended since this date in ISO format (YYYY-MM-DD).")]=None,
    skip: Annotated[str | int,
                    Query(description="Number of records to skip for pagination. E.g. 50 will skip the first 50 records")]=0,
    take: Annotated[str | int | None,
                    Query(description="Number of records to return. E.g. 20 will return the next 20 records after the skipped ones")]=20,
) -> List[Member]:

    # type conversions are necessary for claude to be able to call the api
    house = int(house) if house else None
    skip = int(skip) if skip else 0
    take = int(take) if take else 20

    statement = select(Member).join(Party)
    statement = filter.by_member_name(statement, name)
    statement = filter.by_party(statement, party)
    statement = filter.by_house(statement, house)
    statement = filter.by_membership_start(statement, membership_started_since)
    statement = filter.by_membership_end(statement, membership_ended_since)

    statement = statement.offset(skip).limit(take)

    return list(session.exec(statement).all())

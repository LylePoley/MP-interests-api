from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select, col
from typing import Annotated

from app.models import Party
from app.core.db import get_session

router = APIRouter(prefix="/party", tags=["party"])


@router.get(
    "/search",
    response_model=Party,
    operation_id="search_party",
    description="Search for the information of a political party by their unique id number.",
)
def search_party(
    *,
    session: Session = Depends(get_session),
    party_id: Annotated[str, Query(description="ID of the party to search for. Supports exact matches.")]
) -> Party | None:

    # type conversions are necessary for claude to be able to call the api
    party_id = int(party_id)

    statement = select(Party).where(col(Party.id) == party_id)

    return session.exec(statement).one_or_none()


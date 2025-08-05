from backend.models import Member, Party, Interest, InterestCategory, member_from_dict, interest_from_dict
# from backend.client.mock_clients import mock_interest_client, mock_member_client
from backend.client.fetch import fetch_all_active_members, fetch_all_interests
from backend.client import member_client, interest_client
from backend.core.config import settings, LogLevel

from sqlmodel import SQLModel, create_engine, Session
from typing import Iterable, Iterator
from itertools import batched
from logging import getLogger

logger = getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL.value)

engine = create_engine(settings.SQLITE_DB, echo=settings.LOG_LEVEL == LogLevel.DEBUG)

# for fastapi dependency injection
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)

def merge_members_to_db(data: Iterable[Member], batch_size: int = 100) -> None:
    number_upserted: int = 0
    with Session(engine) as session:
        for member_batch in batched(data, batch_size):
            for member in member_batch:
                if not member.party:
                    logger.warning(f"Member {member.id} has no party.")
                    session.add(member)
                    continue

                db_party = session.get(Party, member.party.id)
                if db_party:
                    member.party = db_party

                session.merge(member)
                number_upserted += 1

            session.commit()
        logger.info(f"Upserted {number_upserted} members.")

def merge_interests_to_db(data: Iterable[Interest], batch_size: int = 100) -> None:
    number_upserted: int = 0
    with Session(engine) as session:
        for interest_batch in batched(data, batch_size):
            for interest in interest_batch:

                db_category = session.get(InterestCategory, interest.category.id) if interest.category else None
                if db_category:
                    interest.category = db_category

                session.merge(interest)
                number_upserted += 1

            session.commit()
        logger.info(f"Upserted {number_upserted} interests.")

def setup_db():
    init_db()

    members_data = fetch_all_active_members(client=member_client)
    members = map(member_from_dict, members_data)
    merge_members_to_db(members)

    interests_data = fetch_all_interests(client=interest_client)
    interests = map(interest_from_dict, interests_data)
    merge_interests_to_db(interests)

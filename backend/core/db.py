from backend.models import Member, Party, Interest, InterestCategory, member_and_party_from_dict, interest_from_dict
# from backend.client.mock_clients import mock_interest_client, mock_member_client
from backend.client.fetch import fetch_all_active_members, fetch_all_interests
from backend.client import member_client, interest_client
from backend.core.config import settings, LogLevel

from sqlmodel import SQLModel, create_engine, Session
from typing import Iterable, Iterator, Tuple
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

def merge_to_db(items: Iterable[Tuple[SQLModel | None, ...]], batch_size: int = 100) -> None:
    number_upserted: int = 0
    with Session(engine) as session:
        for batch in batched(items, batch_size):
            for models in batch:
                for model in models:
                    if model:
                        session.merge(model)
                        number_upserted += 1

            session.commit()
        logger.info(f"Upserted {number_upserted} items.")

def setup_db():
    init_db()

    members_data = fetch_all_active_members(client=member_client)
    parsed_member_data = map(member_and_party_from_dict, members_data)

    merge_to_db(parsed_member_data)

    interests_data = fetch_all_interests(client=interest_client)
    parsed_interests_data = map(interest_from_dict, interests_data)

    merge_to_db(parsed_interests_data)

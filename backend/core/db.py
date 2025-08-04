from sqlmodel import SQLModel, create_engine, Session
from backend.models import Member, Party, Interest, InterestCategory, InterestField
from typing import Iterable
from backend.client.fetch import (
    fetch_all_active_members,
    fetch_all_interests
)
from backend.client import member_client, interest_client
from backend.models import Member, Party, member_from_dict, interest_from_dict
from backend.client.mock_clients import mock_interest_client, mock_member_client

from logging import getLogger

logger = getLogger(__name__)


engine = create_engine("sqlite:///members.db")  # or Postgres URI


def init_db():
    SQLModel.metadata.create_all(engine)


def read_members_to_db(data: Iterable[Member]) -> None:
    with Session(engine) as session:
        for member in data:
            if not member.party:
                logger.warning(f"Member {member.id} has no party.")
                session.add(member)
                continue

            # Check DB in case party already exists
            db_party = session.get(Party, member.party.id)
            if db_party:
                member.party = db_party

            session.add(member)

        session.commit()


def read_interests_to_db(data: Iterable[Interest]) -> None:
    with Session(engine) as session:
        for interest in data:

            db_category = session.get(InterestCategory, interest.category.id) if interest.category else None
            if db_category:
                interest.category = db_category

            session.add(interest)

        session.commit()


def setup_db():
    init_db()

    members_data = fetch_all_active_members(client=member_client)
    members = map(member_from_dict, members_data)
    read_members_to_db(members)

    interests_data = fetch_all_interests(client=interest_client)
    interests = map(interest_from_dict, interests_data)
    read_interests_to_db(interests)


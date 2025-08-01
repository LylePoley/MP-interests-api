from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# ---------- Lookup Tables ----------

class House(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    members: List["Member"] = Relationship(back_populates="house")


class MemberStatus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    notes: Optional[str] = None
    members: List["Member"] = Relationship(back_populates="status")


class GovernmentType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    parties: List["Party"] = Relationship(back_populates="government_type")


# ---------- Party ----------

class Party(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    abbreviation: Optional[str]
    background_colour: Optional[str]
    foreground_colour: Optional[str]
    is_lords_main_party: Optional[bool]
    is_lords_spiritual_party: Optional[bool]
    is_independent_party: Optional[bool]

    government_type_id: Optional[int] = Field(default=None, foreign_key="governmenttype.id")
    government_type: Optional[GovernmentType] = Relationship(back_populates="parties")

    members: List["Member"] = Relationship(back_populates="party")


# ---------- Member ----------

class Member(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_list_as: Optional[str]
    name_display_as: Optional[str]
    name_full_title: Optional[str]
    name_address_as: Optional[str]
    gender: Optional[str]
    thumbnail_url: Optional[str]

    # Membership flattening
    party_id: Optional[int] = Field(default=None, foreign_key="party.id")
    house_id: Optional[int] = Field(default=None, foreign_key="house.id")
    status_id: Optional[int] = Field(default=None, foreign_key="memberstatus.id")

    membership_from: Optional[str]
    membership_from_id: Optional[int]
    membership_start_date: Optional[datetime]
    membership_end_date: Optional[datetime]
    membership_end_reason: Optional[str]
    membership_end_reason_notes: Optional[str]
    membership_end_reason_id: Optional[int]
    status_start_date: Optional[datetime]

    # Relationships
    party: Optional[Party] = Relationship(back_populates="members")
    house: Optional[House] = Relationship(back_populates="members")
    status: Optional[MemberStatus] = Relationship(back_populates="members")

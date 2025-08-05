from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# ---------- Party ----------

class Party(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = None
    abbreviation: str | None = None
    background_colour: str | None = None
    foreground_colour: str | None = None
    is_lords_main_party: bool | None = None
    is_lords_spiritual_party: bool | None = None
    is_independent_party: bool | None = None
    government_type: str | None = None

    members: List["Member"] = Relationship(back_populates="party")


# ---------- Member ----------

class Member(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name_list_as: str | None = None
    name_display_as: str | None = None
    name_full_title: str | None = None
    name_address_as: str | None = None
    gender: str | None = None
    thumbnail_url: str | None = None

    # Membership flattening
    party_id: int | None = Field(default=None, foreign_key="party.id")
    house: int | None = None

    membership_from: str | None = None
    membership_from_id: int | None = None
    membership_start_date: datetime | None = None
    membership_end_date: datetime | None = None
    membership_end_reason: str | None = None
    membership_end_reason_notes: str | None = None
    membership_end_reason_id: int | None = None
    status_is_active: bool | None = None
    status_description: str | None = None
    status_notes: str | None = None
    status_id: int | None = None
    status: int | None = None
    status_start_date: datetime | None = None

    # Relationships
    party: Party | None = Relationship(back_populates="members")
    interests: List["Interest"] = Relationship(back_populates="member")

# ---------- Interest ----------

class InterestCategory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    number: str | None = None
    name: str | None = None


class Interest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    summary: str | None = None

    member_id: int | None = Field(default=None, foreign_key="member.id")
    category_id: int | None = Field(default=None, foreign_key="interestcategory.id")

    registration_date: datetime | None = None
    published_date: datetime | None = None
    rectified: bool | None = None
    rectified_details: str | None = None

    # Relationships
    member: Optional["Member"] = Relationship(back_populates="interests")
    category: Optional["InterestCategory"] = Relationship()
    fields: List["InterestField"] = Relationship(back_populates="interest")
    monetary_value_field: Optional["MonetaryValueField"] = Relationship(back_populates="interest")

    # New parent relationship
    parent_id: Optional[int] = Field(default=None, foreign_key="interest.id")

    # Self-referential relationships
    parent: Optional["Interest"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "Interest.id"})
    children: List["Interest"] = Relationship(back_populates="parent")

Interest.model_rebuild()

# ---------- InterestFields ----------

class InterestField(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    interest_id: int | None = Field(foreign_key="interest.id")

    name: str | None = None
    description: str | None = None
    type: str | None = None

    value: str | None = None  # Can hold serialized value

    interest: Interest = Relationship(back_populates="fields")


# field which contains the monetary value of the interest
class MonetaryValueField(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    interest_id: int | None = Field(foreign_key="interest.id")

    value: float | None = None  # Monetary value in the specified currency
    currency: str | None = None  # Currency code (e.g., 'USD', 'EUR')

    interest: Interest = Relationship(back_populates="monetary_value_field")


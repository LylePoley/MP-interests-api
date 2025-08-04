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


class InterestField(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    interest_id: int | None = Field(foreign_key="interest.id")

    name: str | None = None
    description: str | None = None
    type: str | None = None
    currency: str | None = None

    # Simplified handling of value
    value: str | None = None  # Can hold serialized value

    interest: Interest = Relationship(back_populates="fields")


# class PublishedInterest(BaseModel):
#     """
#     Version of an interest which has been published.
#     """

#     class Config:
#         extra = "forbid"

#     id: Optional[int] = Field(None, description='ID of the interest.')
#     summary: Optional[str] = Field(None, description='Title Summary for the interest.')
#     parentInterestId: Optional[int] = Field(
#         None,
#         description='The unique ID for the payer (parent interest) to which this payment (child interest) is associated.',
#     )
#     registrationDate: Optional[date] = Field(
#         None, description='Registration Date on the published interest.'
#     )
#     publishedDate: Optional[date] = Field(
#         None, description='Date when the interest was first published.'
#     )
#     updatedDates: Optional[List[date]] = Field(
#         None,
#         description='A list of dates on which the interest has been updated since it has been published.',
#     )
#     category: Optional[PublishedCategory] = None
#     member: Optional[Member] = None
#     fields: Optional[List[FieldModel]] = Field(
#         None,
#         description='List of fields which are available for a member to add further information about the interest.',
#     )
#     childInterests: Optional[List[PublishedInterest]] = Field(
#         None,
#         description='List of Interests which are sub interests of this interest. This property is only present if `ExpandChildInterests` is true, and is not defined by default.',
#     )
#     links: Optional[List[Link]] = Field(
#         None,
#         description='A list of HATEOAS Links for retrieving related information about this interest.',
#     )
#     rectified: Optional[bool] = Field(
#         None,
#         description='Whether the interest has been rectified (e.g. when the interest was submitted late).',
#     )
#     rectifiedDetails: Optional[str] = Field(
#         None,
#         description='The reason that the interest was rectified, or `null` if the interest was not rectified.',
#     )

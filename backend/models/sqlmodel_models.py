from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# ---------- Party ----------

class Party(SQLModel, table=True):
    """
    Represents a political party.
    """
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the party")
    name: str | None = Field(default=None, description="Name of the party e.g. 'Conservative'")
    abbreviation: str | None = Field(default=None, description="Abbreviation of the party name e.g. 'Con'")
    background_colour: str | None = Field(default=None, description="Background color associated with the party")
    foreground_colour: str | None = Field(default=None, description="Foreground color associated with the party")
    is_independent_party: bool | None = Field(default=None, description="Indicates if the party is independent")

    members: List["Member"] = Relationship(back_populates="party")


# ---------- Member ----------

class Member(SQLModel, table=True):
    """
    Represents a member of parliament.
    """
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the member")
    name_list_as: str | None = None
    name_display_as: str | None = Field(None, description="Member's current full name, as it should be displayed in text.")
    name_full_title: str | None = Field(None, description="Member's full title, including honorifics.")
    name_address_as: str | None = Field(None, description="Member's name as it should be addressed in correspondence.")
    gender: str | None = Field(None, description="Gender of the member.")
    thumbnail_url: str | None = Field(None, description="URL of the member's thumbnail image.")

    # Membership flattening
    party_id: int | None = Field(default=None, foreign_key="party.id")
    house: int | None = Field(None, description="House the member belongs to (1 for Commons, 2 for Lords)")

    membership_from: str | None = Field(default=None, description="Constituency of Commons Members.")
    membership_from_id: int | None = Field(default=None, description="ID of the constituency for Commons Members.")
    membership_start_date: datetime | None = Field(default=None, description="Date when the member's current membership started.")
    membership_end_date: datetime | None = Field(default=None, description="Date when the member's current membership ended.")
    membership_end_reason: str | None = Field(default=None, description="Reason for the member's current membership ending.")
    status_is_active: bool | None = Field(default=None, description="Indicates if the member is currently active.")
    status_start_date: datetime | None = Field(default=None, description="Date when the member's current status started.")

    # Relationships
    party: Party | None = Relationship(back_populates="members")
    interests: List["Interest"] = Relationship(back_populates="member")

# ---------- Interest ----------

class InterestCategory(SQLModel, table=True):
    """
    Represents a category of interests, for example, 'Gifts, benefits and hospitality from UK sources', 'ad Hoc Payments', etc.
    """
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the interest category")
    number: str | None = Field(default=None, description="Number associated with the interest category")
    name: str | None = Field(default=None, description="Name of the interest category, for example 'Gifts, benefits and hospitality from UK sources'")


class Interest(SQLModel, table=True):
    """
    Represents an interest of a member, such as eployment, directorships, or shareholdings
    """
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the interest")
    summary: str | None = Field(default=None, description="Summary of the interest")

    member_id: int | None = Field(default=None, foreign_key="member.id")
    category_id: int | None = Field(default=None, foreign_key="interestcategory.id")

    registration_date: datetime | None = Field(default=None, description="Date when the interest was registered")
    published_date: datetime | None = Field(default=None, description="Date when the interest was published")
    rectified: bool | None = Field(default=None, description="Indicates if the interest has been rectified")
    rectified_details: str | None = Field(default=None, description="Details regarding the rectification of the interest")

    # Relationships
    member: Optional["Member"] = Relationship(back_populates="interests")
    category: Optional["InterestCategory"] = Relationship()
    fields: List["InterestField"] = Relationship(back_populates="interest")
    monetary_value_field: Optional["MonetaryValueField"] = Relationship(back_populates="interest")

    # New parent relationship
    parent_id: Optional[int] = Field(default=None, foreign_key="interest.id",
        description="ID of the parent interest if this is a child interest e.g. each one off payment from a company is a child of the main interest (employment at that company)")

    # Self-referential relationships
    parent: Optional["Interest"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "Interest.id"})
    children: List["Interest"] = Relationship(back_populates="parent")

Interest.model_rebuild()

# ---------- InterestFields ----------

class InterestField(SQLModel, table=True):
    """
    Field holding information about an interest, such as donor information
    """
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the interest field")
    interest_id: int | None = Field(foreign_key="interest.id")

    name: str | None = Field(default=None, description="Name of the interest field")
    description: str | None = Field(default=None, description="Description of the interest field")
    type: str | None = Field(default=None, description="Type of the fields 'value'")

    value: str | None = Field(default=None, description="Value of field, if applicable. The type of the value is indicated by 'type'")

    interest: Interest = Relationship(back_populates="fields")


# field which contains the monetary value of the interest
class MonetaryValueField(SQLModel, table=True):
    """
    Field holding the monetary value of an interest
    """
    id: int | None = Field(default=None, primary_key=True, description="Unique identifier for the monetary value field")
    interest_id: int | None = Field(foreign_key="interest.id")

    value: float | None = Field(default=None, description="Monetary value in the specified currency")
    currency: str | None = Field(default=None, description="Currency code (e.g., 'USD', 'EUR')")

    interest: Interest = Relationship(back_populates="monetary_value_field")


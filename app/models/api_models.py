from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.models import (
    Member,
    InterestField,
    MonetaryValueField,
    InterestCategory
)

class MemberWithTotalInterestValue(BaseModel):
    member: Member = Field(..., description="Member details")
    total_interests_value: float = Field(
        ..., description="Total value of interests for the member"
    )


class InterestRead(BaseModel):
    id: int | None = Field(
        default=None, description="Unique identifier for the interest"
    )
    category: InterestCategory | None = Field(
        default=None, description="Category of the interest"
    )
    summary: str | None = Field(default=None, description="Summary of the interest")
    registration_date: datetime | None = Field(
        default=None, description="Registration date of the interest"
    )
    published_date: datetime | None = Field(
        default=None, description="Published date of the interest"
    )
    monetary_value_field: MonetaryValueField | None = Field(
        default=None, description="Monetary value field of the interest"
    )
    fields: List[InterestField] = Field(
        ..., description="List of fields associated with the interest"
    )


class MemberWithInterests(BaseModel):
    member: Member = Field(..., description="Member details")
    total_interests_value: float = Field(..., description="Total value of interests for the member")
    interests: List[InterestRead] = Field(
        ..., description="List of interests associated with the member"
    )

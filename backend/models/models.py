from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class GovernmentType(Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_3 = 3

class Party(BaseModel):
    id: int | None = None
    name: str | None = None
    abbreviation: str | None = None
    backgroundColour: str | None = None
    foregroundColour: str | None = None
    isLordsMainParty: bool | None = None
    isLordsSpiritualParty: bool | None = None
    governmentType: GovernmentType | None = None
    isIndependentParty: bool | None = None

class House(Enum):
    integer_1 = 1
    integer_2 = 2

class MemberStatus(Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_3 = 3

class HouseMembershipStatus(BaseModel):
    statusIsActive: bool | None = None
    statusDescription: str | None = None
    statusNotes: str | None = None
    statusId: int | None = None
    status: MemberStatus | None = None
    statusStartDate: datetime | None = None

class HouseMembership(BaseModel):
    membershipFrom: str | None = None
    membershipFromId: int | None = None
    house: House | None = None
    membershipStartDate: datetime | None = None
    membershipEndDate: datetime | None = None
    membershipEndReason: str | None = None
    membershipEndReasonNotes: str | None = None
    membershipEndReasonId: int | None = None
    membershipStatus: HouseMembershipStatus | None = None

class Member(BaseModel):
    id: int | None = None
    nameListAs: str | None = None
    nameDisplayAs: str | None = None
    nameFullTitle: str | None = None
    nameAddressAs: str | None = None
    latestParty: Party | None = None
    gender: str | None = None
    latestHouseMembership: HouseMembership | None = None
    thumbnailUrl: str | None = None

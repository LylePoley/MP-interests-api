from datetime import datetime
from typing import List, Dict
import requests

_BASE_URL = "https://members.parliament.uk"

def get_members(
        name: str | None = None,
        location: str | None = None,
        post_title: str | None = None,
        party_id: int | None = None,
        house: int | None = None,
        constituency_id: int | None = None,
        name_starts_with: str | None = None,
        gender: str | None = None,
        membership_started_since: datetime | None = None,
        membership_ended_since: datetime | None = None,
        membership_end_reason_ids: List[int] | None = None,
        was_member_on_or_after: datetime | None = None,
        was_member_on_or_before: datetime | None = None,
        was_member_of_house: int | None = None,
        is_eligible: bool | None = None,
        is_current_member: bool | None = None,
        policy_interest_id: int | None = None,
        experience: str | None = None,
        skip: int = 0,
        take: int = 20
    ) -> Dict[str, str]:
    """Queries the /api/Members/Search endpoint and returns a list of members."""

    params = {
        "Name": name,
        "Location": location,
        "PostTitle": post_title,
        "PartyId": party_id,
        "House": house,
        "ConstituencyId": constituency_id,
        "NameStartsWith": name_starts_with,
        "Gender": gender,
        "MembershipStartedSince": membership_started_since.isoformat() if membership_started_since else None,
        "MembershipEnded.MembershipEndedSince": membership_ended_since.isoformat() if membership_ended_since else None,
        "MembershipEnded.MembershipEndReasonIds": ",".join(map(str, membership_end_reason_ids)) if membership_end_reason_ids else None,
        "MembershipInDateRange.WasMemberOnOrAfter": was_member_on_or_after.isoformat() if was_member_on_or_after else None,
        "MembershipInDateRange.WasMemberOnOrBefore": was_member_on_or_before.isoformat() if was_member_on_or_before else None,
        "MembershipInDateRange.WasMemberOfHouse": was_member_of_house,
        "IsEligible": str(is_eligible).lower() if is_eligible is not None else None,
        "IsCurrentMember": str(is_current_member).lower() if is_current_member is not None else None,
        "PolicyInterestId": policy_interest_id,
        "Experience": experience,
        "skip": skip,
        "take": min(take, 20)  # API limit
    }

    query = {k: v for k, v in params.items() if v is not None}

    response = requests.get(_BASE_URL + "/api/Members/Search", params=query)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Example usage
    # members = get_members(name="abbot", is_current_member=True, house=1)
    members = requests.get(_BASE_URL + "/api/Members/Search", params={"Name": "abbot"})
    print(members)
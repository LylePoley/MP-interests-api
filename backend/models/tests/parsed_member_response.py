from typing import Dict, Any
from json import loads
from backend.models import Member, Party
from datetime import datetime

parsed_member: Member = Member(
    id=172,
    name_list_as="Abbott, Ms Diane",
    name_display_as="Ms Diane Abbott",
    name_full_title="Rt Hon Diane Abbott MP",
    name_address_as="Ms Abbott",
    gender="F",
    thumbnail_url="https://members-api.parliament.uk/api/Members/172/Thumbnail",
    party_id=8,
    house=1,
    membership_from="Hackney North and Stoke Newington",
    membership_from_id=4074,
    membership_start_date=datetime(1987, 6, 11, 0, 0),
    membership_end_date=None,
    membership_end_reason=None,
    status_is_active=True,
    status_start_date=datetime(2024, 7, 4, 0, 0),
)

parsed_party: Party = Party(
    id=8,
    name="Independent",
    abbreviation="Ind",
    background_colour="909090",
    foreground_colour="FFFFFF",
    is_independent_party=True,
)

member_response_data: Dict[str, Any] = loads(
    """
{
    "value": {
    "id": 172,
    "nameListAs": "Abbott, Ms Diane",
    "nameDisplayAs": "Ms Diane Abbott",
    "nameFullTitle": "Rt Hon Diane Abbott MP",
    "nameAddressAs": "Ms Abbott",
    "latestParty": {
        "id": 8,
        "name": "Independent",
        "abbreviation": "Ind",
        "backgroundColour": "909090",
        "foregroundColour": "FFFFFF",
        "isLordsMainParty": false,
        "isLordsSpiritualParty": false,
        "governmentType": null,
        "isIndependentParty": true
    },
    "gender": "F",
    "latestHouseMembership": {
        "membershipFrom": "Hackney North and Stoke Newington",
        "membershipFromId": 4074,
        "house": 1,
        "membershipStartDate": "1987-06-11T00:00:00",
        "membershipEndDate": null,
        "membershipEndReason": null,
        "membershipEndReasonNotes": null,
        "membershipEndReasonId": null,
        "membershipStatus": {
        "statusIsActive": true,
        "statusDescription": "Current Member",
        "statusNotes": null,
        "statusId": 0,
        "status": 0,
        "statusStartDate": "2024-07-04T00:00:00"
        }
    },
    "thumbnailUrl": "https://members-api.parliament.uk/api/Members/172/Thumbnail"
    },
    "links": [
    {
        "rel": "self",
        "href": "/Members/172",
        "method": "GET"
    },
    {
        "rel": "overview",
        "href": "/Members/172",
        "method": "GET"
    },
    {
        "rel": "synopsis",
        "href": "/Members/172/Synopsis",
        "method": "GET"
    },
    {
        "rel": "contactInformation",
        "href": "/Members/172/Contact",
        "method": "GET"
    }
    ]
}
"""
)

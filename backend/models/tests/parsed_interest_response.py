from typing import Dict, Any, List
from json import loads
from backend.models import Interest, InterestCategory, InterestField, MonetaryValueField
from datetime import datetime


parsed_interest_category: InterestCategory = InterestCategory(
    id=4,
    number="3",
    name="Gifts, benefits and hospitality from UK sources",
)

parsed_monetary_value_field: MonetaryValueField = MonetaryValueField(
    interest_id=12880, currency="GBP", value=1396.00
)

parsed_interest_fields: List[InterestField] = [
    InterestField(
        interest_id=12880,
        name="Appg",
        description="Whether the benefit was via an All Parliamentary Group (APPG)",
        type="String",
        value=None,
    ),
    InterestField(
        interest_id=12880,
        name="PaymentType",
        description="Whether the benefit was monetary or in kind",
        type="String",
        value="In kind",
    ),
    InterestField(
        interest_id=12880,
        name="PaymentDescription",
        description="Description of the payment",
        type="String",
        value="Event tickets and hospitality in The Royal Box at the Wimbledon Championship for myself and 1 other.",
    ),
    InterestField(
        interest_id=12880,
        name="ReceivedDate",
        description="Date on which the benefit was received",
        type="DateOnly",
        value="2025-07-12",
    ),
    InterestField(
        interest_id=12880,
        name="AcceptedDate",
        description="Date on which the benefit was accepted",
        type="DateOnly",
        value="2025-07-12",
    ),
    InterestField(
        interest_id=12880,
        name="ReceivedEndDate",
        description="End date, if the benefit was received over time",
        type="DateOnly",
        value=None,
    ),
    InterestField(
        interest_id=12880,
        name="IsSoleBeneficiary",
        description="Whether Member is the sole beneficiary",
        type="Boolean",
        value=False,
    ),
    InterestField(
        interest_id=12880,
        name="DonorName",
        description="Name of the donor",
        type="String",
        value="The All England Lawn Tennis Club (CHAMPIONSHIPS) Limited",
    ),
    InterestField(
        interest_id=12880,
        name="DonorPublicAddress",
        description="Address of the donor, if this can be publicly shared",
        type="String",
        value="Church Road, Wimbledon SW19 5AE",
    ),
    InterestField(
        interest_id=12880,
        name="DonorStatus",
        description="Status of the donor",
        type="String",
        value="Company",
    ),
    InterestField(
        interest_id=12880,
        name="DonorCompanyName",
        description="Name of the donor company",
        type="String",
        value="The All England Lawn Tennis Club (CHAMPIONSHIPS) Limited",
    ),
    InterestField(
        interest_id=12880,
        name="DonorCompanyUrl",
        description="URL of the donor company",
        type="String",
        value=None,
    ),
    InterestField(
        interest_id=12880,
        name="DonorCompanyIdentifier",
        description="Company registration number",
        type="String",
        value="7546773",
    ),
    InterestField(
        interest_id=12880,
        name="DonorCompanyIdentifierSource",
        description="Source of company identifier",
        type="String",
        value="Companies House",
    ),
    InterestField(
        interest_id=12880,
        name="DonorTrustDetails",
        description="Details of the trust",
        type="String",
        value=None,
    ),
    InterestField(
        interest_id=12880,
        name="DonorOtherDetails",
        description="Description of donor status, where this could not be covered by defined options",
        type="String",
        value=None,
    ),
]

parsed_interest: Interest = Interest(
    id=12880,
    summary="The All England Lawn Tennis Club (CHAMPIONSHIPS) Limited - £1,396.00",
    registration_date=datetime(2025, 7, 14),
    published_date=datetime(2025, 7, 14),
    member_id=4597,
    category_id=4,
    rectified=False,
    rectified_details=None,
)


interest_response_data: Dict[str, Any] = loads(
    """
{
    "id": 12880,
    "summary": "The All England Lawn Tennis Club (CHAMPIONSHIPS) Limited - £1,396.00",
    "parentInterestId": null,
    "registrationDate": "2025-07-14",
    "publishedDate": "2025-07-14",
    "updatedDates": [],
    "category": {
    "id": 4,
    "number": "3",
    "name": "Gifts, benefits and hospitality from UK sources",
    "parentCategoryIds": [],
    "type": "Commons",
    "links": [
        {
        "rel": "self",
        "href": "https://interests-api.parliament.uk/api/v1/Categories/4",
        "method": "GET"
        }
    ]
    },
    "member": {
        "id": 4597,
        "nameDisplayAs": "Mrs Kemi Badenoch",
        "nameListAs": "Badenoch, Mrs Kemi",
        "house": "Commons",
        "memberFrom": "North West Essex",
        "party": "Conservative",
        "links": [
            {
            "rel": "self",
            "href": "https://members-api.parliament.uk/api/Members/4597",
            "method": "GET"
            }
        ]
    },
    "fields": [
    {
        "name": "Appg",
        "description": "Whether the benefit was via an All Parliamentary Group (APPG)",
        "type": "String",
        "typeInfo": null,
        "value": null
    },
    {
        "name": "PaymentType",
        "description": "Whether the benefit was monetary or in kind",
        "type": "String",
        "typeInfo": null,
        "value": "In kind"
    },
    {
        "name": "PaymentDescription",
        "description": "Description of the payment",
        "type": "String",
        "typeInfo": null,
        "value": "Event tickets and hospitality in The Royal Box at the Wimbledon Championship for myself and 1 other."
    },
    {
        "name": "Value",
        "description": "Value of the benefit",
        "type": "Decimal",
        "typeInfo": {
        "currencyCode": "GBP"
        },
        "value": "1396.00"
    },
    {
        "name": "ReceivedDate",
        "description": "Date on which the benefit was received",
        "type": "DateOnly",
        "typeInfo": null,
        "value": "2025-07-12"
    },
    {
        "name": "AcceptedDate",
        "description": "Date on which the benefit was accepted",
        "type": "DateOnly",
        "typeInfo": null,
        "value": "2025-07-12"
    },
    {
        "name": "ReceivedEndDate",
        "description": "End date, if the benefit was received over time",
        "type": "DateOnly",
        "typeInfo": null,
        "value": null
    },
    {
        "name": "IsSoleBeneficiary",
        "description": "Whether Member is the sole beneficiary",
        "type": "Boolean",
        "typeInfo": null,
        "value": false
    },
    {
        "name": "DonorName",
        "description": "Name of the donor",
        "type": "String",
        "typeInfo": null,
        "value": "The All England Lawn Tennis Club (CHAMPIONSHIPS) Limited"
    },
    {
        "name": "DonorPublicAddress",
        "description": "Address of the donor, if this can be publicly shared",
        "type": "String",
        "typeInfo": null,
        "value": "Church Road, Wimbledon SW19 5AE"
    },
    {
        "name": "DonorStatus",
        "description": "Status of the donor",
        "type": "String",
        "typeInfo": null,
        "value": "Company"
    },
    {
        "name": "DonorCompanyName",
        "description": "Name of the donor company",
        "type": "String",
        "typeInfo": null,
        "value": "The All England Lawn Tennis Club (CHAMPIONSHIPS) Limited"
    },
    {
        "name": "DonorCompanyUrl",
        "description": "URL of the donor company",
        "type": "String",
        "typeInfo": null,
        "value": null
    },
    {
        "name": "DonorCompanyIdentifier",
        "description": "Company registration number",
        "type": "String",
        "typeInfo": null,
        "value": "7546773"
    },
    {
        "name": "DonorCompanyIdentifierSource",
        "description": "Source of company identifier",
        "type": "String",
        "typeInfo": null,
        "value": "Companies House"
    },
    {
        "name": "DonorTrustDetails",
        "description": "Details of the trust",
        "type": "String",
        "typeInfo": null,
        "value": null
    },
    {
        "name": "DonorOtherDetails",
        "description": "Description of donor status, where this could not be covered by defined options",
        "type": "String",
        "typeInfo": null,
        "value": null
    }
    ],
    "links": [
    {
        "rel": "self",
        "href": "https://interests-api.parliament.uk/api/v1/Interests/12880",
        "method": "GET"
    }
    ],
    "rectified": false,
    "rectifiedDetails": null
}
"""
)

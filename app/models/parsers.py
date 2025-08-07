from typing import Dict, Any, List, Tuple
from app.models import (
    Member,
    Party,
    Interest,
    InterestCategory,
    InterestField,
    MonetaryValueField,
)
from datetime import datetime
from sqlmodel import SQLModel



def deep_get(data: Dict[str, Any], path: List[str], default: Any = None) -> Any:
    current: Any = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return default

    return current


def parse_date(date_str: str | None) -> datetime | None:
    return datetime.fromisoformat(date_str) if date_str else None


def member_and_party_from_dict(data: Dict[str, Any]) -> Tuple[Member, Party]:
    party = Party(
        id=deep_get(data, ["value", "latestParty", "id"]),
        name=deep_get(data, ["value", "latestParty", "name"]),
        abbreviation=deep_get(data, ["value", "latestParty", "abbreviation"]),
        background_colour=deep_get(data, ["value", "latestParty", "backgroundColour"]),
        foreground_colour=deep_get(data, ["value", "latestParty", "foregroundColour"]),
        is_independent_party=deep_get(
            data, ["value", "latestParty", "isIndependentParty"]
        ),
    )

    member = Member(
        id=deep_get(data, ["value", "id"]),
        name_list_as=deep_get(data, ["value", "nameListAs"]),
        name_display_as=deep_get(data, ["value", "nameDisplayAs"]),
        name_full_title=deep_get(data, ["value", "nameFullTitle"]),
        name_address_as=deep_get(data, ["value", "nameAddressAs"]),
        gender=deep_get(data, ["value", "gender"]),
        thumbnail_url=deep_get(data, ["value", "thumbnailUrl"]),
        party_id=deep_get(data, ["value", "latestParty", "id"]),
        house=deep_get(data, ["value", "latestHouseMembership", "house"]),
        membership_from=deep_get(
            data, ["value", "latestHouseMembership", "membershipFrom"]
        ),
        membership_from_id=deep_get(
            data, ["value", "latestHouseMembership", "membershipFromId"]
        ),
        membership_start_date=parse_date(
            deep_get(data, ["value", "latestHouseMembership", "membershipStartDate"])
        ),
        membership_end_date=parse_date(
            deep_get(data, ["value", "latestHouseMembership", "membershipEndDate"])
        ),
        membership_end_reason=deep_get(
            data, ["value", "latestHouseMembership", "membershipEndReason"]
        ),
        status_is_active=deep_get(
            data,
            ["value", "latestHouseMembership", "membershipStatus", "statusIsActive"],
        ),
        status_start_date=parse_date(
            deep_get(
                data,
                [
                    "value",
                    "latestHouseMembership",
                    "membershipStatus",
                    "statusStartDate",
                ],
            )
        ),
    )

    return member, party


def interest_from_dict(data: Dict[str, Any]) -> Tuple[SQLModel | None, ...]:
    category = InterestCategory(
        id=deep_get(data, ["category", "id"]),
        number=deep_get(data, ["category", "number"]),
        name=deep_get(data, ["category", "name"]),
    )

    fields: List[InterestField] = []
    monetary_value_field: MonetaryValueField | None = None

    for field in data.get("fields", []):
        if deep_get(field, ["typeInfo", "currencyCode"]):
            monetary_value_field = MonetaryValueField(
                interest_id=data.get("id"),
                value=field.get("value"),
                currency=deep_get(field, ["typeInfo", "currencyCode"]),
            )
            continue

        fields.append(
            InterestField(
                interest_id=data.get("id"),
                name=field.get("name"),
                description=field.get("description"),
                type=field.get("type", {}),
                value=field.get("value"),
            )
        )

    interest = Interest(
        id=data.get("id"),
        parent_id=data.get("parentInterestId"),
        summary=data.get("summary"),
        member_id=deep_get(data, ["member", "id"]),
        category_id=category.id,
        registration_date=parse_date(data.get("registrationDate")),
        published_date=parse_date(data.get("publishedDate")),
        rectified=data.get("rectified"),
        rectified_details=data.get("rectifiedDetails"),
        category=category,
        fields=fields,
        monetary_value_field=monetary_value_field,
    )

    return interest, category, *fields, monetary_value_field


if __name__ == "__main__":
    ...

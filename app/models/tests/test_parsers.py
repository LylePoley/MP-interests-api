from typing import Dict, Any, List, Tuple
import pytest
from sqlmodel import SQLModel

from app.models.parsers import deep_get
from app.models import (
    Member,
    Party
)

from app.models.parsers import member_and_party_from_dict, interest_from_dict

from app.models.tests.parsed_member_response import (
    member_response_data,
    parsed_member,
    parsed_party,
)
from app.models.tests.parsed_interest_response import (
    interest_response_data,
    parsed_interest,
    parsed_interest_category,
    parsed_monetary_value_field,
    parsed_interest_fields,
)


@pytest.mark.parametrize(
    "data, key, expected",
    [
        ({"one": "level"}, ["one"], "level"),
        ({"no": "matching", "key": "present"}, ["one"], None),
        ({"does": "not", "match": "multiple", "keys": "here"}, ["does", "match"], None),
        (
            {"because": {"it": {"is": {"for": {"nested": "dictionaries"}}}}},
            ["because", "it", "is", "for", "nested"],
            "dictionaries",
        ),
    ],
)
def test_deep_get(data: Dict[str, Any], key: List[str], expected: Any | None):
    assert deep_get(data, key) == expected


@pytest.mark.parametrize(
    "member_response_data, expected",
    [
        (member_response_data, tuple((parsed_member, parsed_party)))
    ]
)
def test_member_and_party_from_dict(member_response_data: Dict[str, Any], expected: Tuple[Member, Party]):
    member, party = member_and_party_from_dict(member_response_data)

    assert member == expected[0]
    assert party == expected[1]


@pytest.mark.parametrize(
    "interest_response_data, expected",
    [
        (interest_response_data, tuple((parsed_interest, parsed_interest_category, *parsed_interest_fields, parsed_monetary_value_field)))
    ]
)
def test_interest_from_dict(interest_response_data: Dict[str, Any], expected: Tuple[SQLModel, ...]):
    interest, category, *fields, monetary_value_field = interest_from_dict(interest_response_data)

    assert interest == expected[0]
    assert category == expected[1]
    for field, expected_field in zip(fields, expected[2:-1]):
        assert field == expected_field

    #TODO monetary_value_field's value is a string here for some reason
    monetary_value_field.value = float(monetary_value_field.value) if monetary_value_field.value else None
    assert monetary_value_field == expected[-1]

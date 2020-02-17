import sys
import random

import pytest

from typing import List
from dataclasses import dataclass

from hypothesis import assume, given
from hypothesis import strategies as st

from testplates import OneOf, Contains, Length, MatchesString, MatchesBytes


@given(values=st.lists(st.integers(), min_size=1))
def test_one_of(values: List[int]) -> None:
    value = random.choice(values)

    assert OneOf(*values) == value


@given(values=st.lists(st.integers(), min_size=1))
def test_contains(values: List[int]) -> None:
    number_of_samples = random.randint(1, len(values))
    samples = random.sample(values, k=number_of_samples)

    assert Contains(*samples) == values


@given(values=st.lists(st.integers()))
def test_contains_always_returns_true_without_values(values: List[int]) -> None:
    assert Contains() == values


def test_contains_always_returns_false_when_value_is_not_a_container() -> None:
    class Custom:

        __contains__ = None

    assert Contains() != Custom()


@given(values=st.lists(st.integers(), min_size=1), extra_value=st.integers())
def test_contains_returns_false_when_at_least_one_value_is_not_inside_values(
    values: List[int], extra_value: int
) -> None:
    assume(extra_value not in values)

    number_of_samples = random.randint(1, len(values))
    samples = random.sample(values, k=number_of_samples)
    samples.append(extra_value)

    assert Contains(*samples) != values


@given(length=st.integers(min_value=0, max_value=sys.maxsize))
def test_length(length: int) -> None:
    @dataclass
    class Value:

        length: int

        def __len__(self) -> int:
            return self.length

    assert Length(length) == Value(length)


@given(length=st.integers())
def test_length_always_returns_false_when_value_is_not_sized(length: int) -> None:
    class Custom:

        __len__ = None

    assert Length(length) != Custom()


@given(data=st.data())
@pytest.mark.parametrize("pattern", [r"\d+"])
def test_matches_string(data: st.DataObject, pattern: str) -> None:
    value = data.draw(st.from_regex(pattern, fullmatch=True))

    assert MatchesString(pattern) == value


@given(data=st.data())
@pytest.mark.parametrize("pattern", [r"\d+"])
def test_matches_string_always_returns_false_on_str_value(
    data: st.DataObject, pattern: str
) -> None:
    value = data.draw(st.from_regex(pattern, fullmatch=True))

    assert MatchesString(pattern) != value.encode()


@given(data=st.data())
@pytest.mark.parametrize("pattern", [rb"\d+"])
def test_matches_bytes(data: st.DataObject, pattern: bytes) -> None:
    value = data.draw(st.from_regex(pattern, fullmatch=True))

    assert MatchesBytes(pattern) == value


@given(data=st.data())
@pytest.mark.parametrize("pattern", [rb"\d+"])
def test_matches_bytes_always_returns_false_on_str_value(
    data: st.DataObject, pattern: bytes
) -> None:
    value = data.draw(st.from_regex(pattern, fullmatch=True))

    assert MatchesBytes(pattern) != value.decode()
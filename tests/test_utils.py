import pytest

from api.utils import (
    is_lowercase_roman_numeral,
    is_single_lowercase_alpha,
    lowercase_alpha_to_int,
    lowercase_roman_to_int,
)


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("a", True),
        ("z", True),
        ("A", False),
        ("ab", False),
        ("", False),
        ("1", False),
    ],
)
def test_is_single_lowercase_alpha(input_str, expected):
    assert is_single_lowercase_alpha(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("i", True),
        ("ii", True),
        ("iv", True),
        ("xl", True),
        ("cm", True),
        ("abc", False),
        ("ivxlcdm", True),
        ("I", False),
        ("ivxLCDM", False),
    ],
)
def test_is_lowercase_roman_numeral(input_str, expected):
    assert is_lowercase_roman_numeral(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("i", 1),
        ("ii", 2),
        ("iii", 3),
        ("iv", 4),
        ("v", 5),
        ("vi", 6),
        ("vii", 7),
        ("viii", 8),
        ("ix", 9),
        ("x", 10),
        ("xi", 11),
        ("xx", 20),
        ("xl", 40),
        ("l", 50),
        ("lx", 60),
        ("xc", 90),
        ("c", 100),
        ("cd", 400),
        ("d", 500),
        ("cm", 900),
        ("m", 1000),
        ("mmxxiii", 2023),
    ],
)
def test_roman_to_int(input_str, expected):
    assert lowercase_roman_to_int(input_str) == expected


@pytest.mark.parametrize(
    "input_letter,expected",
    [
        ("a", 1),
        ("b", 2),
        ("c", 3),
        ("z", 26),
    ],
)
def test_letter_to_int(input_letter, expected):
    assert lowercase_alpha_to_int(input_letter) == expected

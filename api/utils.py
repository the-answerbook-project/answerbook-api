import re

LOWER_ROMAN_NUMERAL = r"^[ivxlcdm]+$"
EXTENSION = r"^(\d+)\s*(minutes)?$"


def is_single_lowercase_alpha(s: str) -> bool:
    return len(s) == 1 and s.islower()


def is_lowercase_roman_numeral(s: str) -> bool:
    roman_numeral_pattern = re.compile(LOWER_ROMAN_NUMERAL)
    return bool(roman_numeral_pattern.match(s))


def lowercase_roman_to_int(s: str) -> int:
    roman_numerals = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}
    total, prev_value = 0, 0

    for char in reversed(s):
        value = roman_numerals[char]
        total += value if value >= prev_value else -value
        prev_value = value

    return total


def lowercase_alpha_to_int(letter):
    return ord(letter.lower()) - ord("a") + 1


def parse_extension(extension: str) -> int:
    """
    Parse a string of the form 'n' or 'n minutes' into the corresponding integer for 'n'
    to be interpreted as a duration in minutes to add to the nominal duration of the corresponding assessment.
    """
    if match := re.compile(EXTENSION).match(extension):
        return int(match.group(1))
    raise ValueError(f"Invalid extension: '{extension}'")

import re


def is_single_lowercase_alpha(s: str) -> bool:
    return len(s) == 1 and s.islower()


def is_lowercase_roman_numeral(s: str) -> bool:
    roman_numeral_pattern = re.compile(r"^[ivxlcdm]+$")
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

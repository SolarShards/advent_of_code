import re


def read_input(filename: str) -> list[str]:
    return open(filename).readlines()


def count_nice_strings(strings: list[str], nice_pattern: re.Pattern) -> int:
    return len([None for s in strings if re.match(nice_pattern, s)])


def part_one(filename: str) -> int:
    return count_nice_strings(
        read_input(filename),
        re.compile(
            r"""
            (?!.*ab|.*cd|.*pq|.*xy)
            (?=.*(.)\1)
            (?=.*[aeiou].*[aeiou].*[aeiou])""",
            re.VERBOSE
        )
    )


def part_two(filename: str) -> int:
    return count_nice_strings(
        read_input(filename),
        re.compile(
            r"""(?=(?:.*([a-zA-Z]{2}).*\1))(?=(?:.*([a-zA-Z]).\2)).*""",
            re.VERBOSE
        )
    )

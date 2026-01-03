import re

MIN, MAX, FORBIDDEN = ord('a'), ord('z'), (ord('i'), ord('o'), ord('l'))
pattern = re.compile(
        r"""
        (?=.*(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz))
        (?=(?:.*([a-z])\1.*([a-z])\2)).*""",
        re.VERBOSE
    )


def read_input(filename: str) -> str:
    return "hxbxwxba"


def increment_all_forbidden(string: str) -> str:
    chars = [ord(ch) for ch in reversed(string)]
    for idx in range(len(chars)):
        if chars[idx] in FORBIDDEN:
            chars[idx] += 1
            for i in range(idx):
                chars[i] = MIN
    return "".join(chr(ch) for ch in reversed(chars))


def increment(string: str) -> str:
    chars = [ord(ch) for ch in reversed(string)]
    for idx in range(len(chars)):
        chars[idx] += 1
        if chars[idx] in FORBIDDEN:
            chars[idx] += 1
            for i in range(idx):
                chars[i] = MIN
            break
        elif chars[idx] > MAX:
            chars[idx] = MIN
            for i in range(idx):
                chars[i] = MIN
        else:
            break
    return "".join(chr(ch) for ch in reversed(chars))


def part_one(filename: str) -> str:
    pwd = increment_all_forbidden(read_input(filename))
    while not re.match(pattern, pwd := increment(pwd)):
        pass
    return pwd


def part_two(filename: str) -> str:
    pwd = increment(part_one(filename))
    while not re.match(pattern, pwd := increment(pwd)):
        pass
    return pwd

import re


def read_input(filename: str) -> str:
    return "1113122113"


def look_and_say(sequence: str, iterations: int) -> str:
    for _ in range(iterations):
        sequence = "".join(
            str(len(grp[0])) + grp[1]
            for grp in re.findall(r"(?:((.)\2*))", sequence)
        )
    return sequence


def part_one(filename: str) -> int:
    return len(look_and_say(read_input(filename), 40))


def part_two(filename: str) -> int:
    return len(look_and_say(read_input(filename), 50))


if __name__ == "__main__":
    import os
    print(part_two(os.path.dirname(__file__) + "\\input.txt"))

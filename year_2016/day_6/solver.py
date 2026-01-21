from typing import Callable


def read_input(filename: str) -> list[str]:
    return [line.strip() for line in open(filename)]


def correct_message(repetitions: list[str], function: Callable):
    return "".join([
        function(list(set(chars)), key=lambda c: chars.count(c))
        for chars in zip(*repetitions)
    ])


def part_one(filename: str) -> str:
    return correct_message(read_input(filename), max)


def part_two(filename: str) -> str:
    return correct_message(read_input(filename), min)

from operator import add, sub
from dataclasses import dataclass
from typing import Callable


@dataclass
class Rotation:
    move: Callable
    clicks: int


def read_input(filename: str) -> list[Rotation]:
    with open(filename) as file:
        return [
            Rotation(add if line[0] == "R" else sub, int(line[1:]))
            for line in file
        ]


def part_one(filename: str) -> int:
    instructions = read_input(filename)
    position = 50
    password = 0

    for inst in instructions:
        position = inst.move(position, inst.clicks) % 100
        if position == 0:
            password += 1

    return password


def part_two_bruteforce(filename: str) -> int:
    instructions = read_input(filename)
    position = 50
    password = 0

    for inst in instructions:
        new_pos = inst.move(position, inst.clicks)
        step = 1 if inst.move == add else -1
        for i in range(position + step, new_pos + step, step):
            if not i % 100:
                password += 1
        position = new_pos % 100

    return password


def part_two(filename: str) -> int:
    instructions = read_input(filename)
    position = 50
    password = 0

    for inst in instructions:
        new_pos = inst.move(position, inst.clicks)
        password += abs(new_pos) // 100 + int(position > 0 and new_pos <= 0)
        position = new_pos % 100

    return password

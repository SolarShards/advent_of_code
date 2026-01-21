import os
from typing import Callable


def rect(screen: list[list[bool]], width: int, height: int):
    for row in range(height):
        for col in range(width):
            screen[row][col] = True


def rotate_row(screen: list[list[bool]], row: int, shift: int):
    screen[row] = screen[row][-shift:] + screen[row][:-shift]


def rotate_col(screen: list[list[bool]], col: int, shift: int):
    pixels = [row[col] for row in screen]
    pixels = pixels[-shift:] + pixels[:-shift]
    for row in range(len(screen)):
        screen[row][col] = pixels[row]


def swipe_card(card: list[tuple[Callable, int, int]]) -> list[list[bool]]:
    screen = [[False]*50 for _ in range(6)]
    for operation, arg1, arg2 in card:
        operation(screen, arg1, arg2)
    return screen


def read_input(filename: str) -> list[tuple[Callable, int, int]]:
    ops = {"rect": rect, "row": rotate_row, "column": rotate_col}
    instructions: list[tuple[Callable, int, int]] = []
    for inst in [line.split() for line in open(filename)]:
        if inst[0] == "rect":
            x, y = inst[1].split('x')
            instructions.append((ops[inst[0]], int(x), int(y)))
        elif inst[0] == "rotate":
            instructions.append((ops[inst[1]], int(inst[2][2:]), int(inst[4])))
    return instructions


def part_one(filename: str) -> int:
    return sum([sum(row) for row in swipe_card(read_input(filename))])


def part_two(filename: str) -> int:
    with open(os.path.dirname(__file__) + "/part_2_answer.txt", 'w') as f:
        f.writelines([
            "".join(["#" if pixel else " " for pixel in row]) + "\n"
            for row in swipe_card(read_input(filename))
        ])
    return 0

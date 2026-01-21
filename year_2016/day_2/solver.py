from operator import add


def read_input(filename: str) -> list[list[tuple[int, int]]]:
    movement_map = {"U": (-1, 0), "D": (+1, 0), "L": (0, -1), "R": (0, +1)}
    return [[movement_map[m] for m in line.strip()] for line in open(filename)]


def find_keypad_code(
        keypad: list[str],
        start: tuple[int, int],
        instructions: list[list[tuple[int, int]]]) -> str:
    position, code = start, ""
    for sequence in instructions:
        for move in sequence:
            new_position = tuple(map(add, position, move))
            if new_position[0] in range(len(keypad))\
                    and new_position[1] in range(len(keypad[new_position[0]]))\
                    and keypad[new_position[0]][new_position[1]] != " ":
                position = new_position
        code += keypad[position[0]][position[1]]
    return code


def part_one(filename: str) -> str:
    keypad = ["123", "456", "789"]
    return find_keypad_code(keypad, (1, 1), read_input(filename))


def part_two(filename: str) -> str:
    keypad = ["  1  ", " 234 ", "56789", " ABC ", "  D  "]
    return find_keypad_code(keypad, (2, 0), read_input(filename))

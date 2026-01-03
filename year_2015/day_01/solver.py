def read_input(filename: str) -> str:
    return open(filename).read()


def part_one(filename: str) -> int:
    instructions = read_input(filename)
    print(instructions)
    return instructions.count("(") - instructions.count(")")


def part_two(filename: str) -> int:
    instructions = read_input(filename)
    floor = 0
    pos = 0
    while floor != -1:
        floor += 1 if instructions[pos] == "(" else -1
        pos += 1
    return pos

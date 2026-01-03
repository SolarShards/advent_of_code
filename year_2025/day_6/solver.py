from math import prod


def read_input(filename: str) -> list[str]:
    return open(filename).readlines()


def part_one(filename: str) -> int:
    problems = read_input(filename)
    operands = list(zip(*[map(int, line.split()) for line in problems[:-1]]))
    operators = [sum if op == '+' else prod for op in problems[-1].split()]
    return sum(
        operator(numbers) for numbers, operator in zip(operands, operators)
    )


def part_two(filename: str) -> int:
    problems = read_input(filename)
    operands = list[list[int]]()
    block = list[int]()
    for col in list(zip(*map(list, problems[:-1]))):
        s = ''.join(col)
        if s.isspace():
            operands.append(block)
            block = []
        else:
            block.append(int(s.strip()))

    operators = [sum if op == "+" else prod for op in problems[-1].split()]
    return sum(
        operator(numbers) for numbers, operator in zip(operands, operators)
    )

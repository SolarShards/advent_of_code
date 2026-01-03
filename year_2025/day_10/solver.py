import z3


def read_input(
        filename: str
        ) -> list[tuple[int, tuple[tuple[int, ...], ...], tuple[int, ...]]]:
    return [
        (
            sum(1 << i for i, ch in enumerate(line[0][1:-1]) if ch == "#"),
            tuple([
                tuple(map(int, b[1:-1].split(',')))
                for b in line[1:-1]
            ]),
            tuple(map(int, line[-1][1:-1].split(',')))
        )
        for line in [line.split() for line in open(filename).readlines()]
    ]


def part_one(filename: str) -> int:
    presses = 0
    for (target, buttons, _) in read_input(filename):
        btns = [sum(1 << i for i in button) for button in buttons]
        states = {0}
        while target not in states:
            states = set(state ^ btn for state in states for btn in btns)
            presses += 1
    return presses


def part_two(filename: str) -> int:
    presses = 0
    for (_, buttons, target) in read_input(filename):
        variables = z3.IntVector("x", len(buttons))
        solver = z3.Optimize()
        solver.add(variable >= 0 for variable in variables)
        solver.add(
            z3.Sum(
                [variables[j] for j, btn in enumerate(buttons) if i in btn]
            ) == joltage
            for i, joltage in enumerate(target)
        )
        solutions = z3.Sum(variables)
        solver.minimize(solutions)
        solver.check()
        presses += solver.model().eval(solutions).as_long()  # type: ignore

    return presses

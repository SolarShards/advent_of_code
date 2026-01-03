def read_input(filename: str) -> tuple[tuple[int, int], ...]:
    directions = {
        "<": (-1, 0),
        ">": (+1, 0),
        "^": (0, -1),
        "v": (0, +1)
    }
    return tuple(directions[ch] for ch in open(filename).read())


def add_coords(a: tuple[int, int], b: tuple[int, int]):
    return (a[0] + b[0], a[1] + b[1])


def part_one(filename: str) -> int:
    directions = read_input(filename)
    visited = [(0, 0)]
    for direction in directions:
        visited.append(add_coords(visited[-1], direction))
    return len(set(visited))


def part_two(filename: str) -> int:
    directions = read_input(filename)
    santa_visited = [(0, 0)]
    robo_visited = [(0, 0)]
    for i in range(0, len(directions), 2):
        santa_visited.append(add_coords(santa_visited[-1], directions[i]))
        robo_visited.append(add_coords(robo_visited[-1], directions[i+1]))
    return len(set(santa_visited + robo_visited))

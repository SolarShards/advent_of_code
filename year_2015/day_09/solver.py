from itertools import permutations, pairwise


def read_input(filename: str) -> dict[str, dict[str, int]]:
    graph: dict[str, dict[str, int]] = {}
    for start, dest, distance in [ln.split()[::2] for ln in open(filename)]:
        if start not in graph:
            graph[start] = {}
        if dest not in graph:
            graph[dest] = {}
        graph[start][dest] = int(distance)
        graph[dest][start] = int(distance)
    return graph


def part_one(filename: str) -> int:
    graph = read_input(filename)
    return min([
        sum(graph[start][dest] for start, dest in pairwise(order))
        for order in permutations(graph.keys())
    ])


def part_two(filename: str):
    graph = read_input(filename)
    return max([
        sum(graph[start][dest] for start, dest in pairwise(order))
        for order in permutations(graph.keys())
    ])

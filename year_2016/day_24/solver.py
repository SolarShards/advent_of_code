import heapq
from itertools import permutations, pairwise
from dataclasses import dataclass


@dataclass
class Node:
    x: int
    y: int
    steps: int

    def same_pos(self, other: 'Node') -> bool:
        return self.x == other.x and self.y == other.y

    def __gt__(self, other: 'Node') -> bool:
        return self.steps >= other.steps


def find_distances(
        maze: list[list[str]],
        numbers: dict[str, tuple[int, int]]) -> dict[str, dict[str, int]]:
    distances = {i: {} for i in numbers}
    for number, others in distances.items():
        open_list, closed_list = [Node(*numbers[number], 0)], []
        heapq.heapify(open_list)
        while (len(others) < len(numbers) - 1) and open_list:
            node = heapq.heappop(open_list)
            s = node.steps + 1
            for n in (
                        Node(node.x+1, node.y, s),
                        Node(node.x-1, node.y, s),
                        Node(node.x, node.y+1, s),
                        Node(node.x, node.y-1, s)
                    ):
                loc = maze[n.y][n.x]
                if loc == '#':
                    continue
                for known_node in open_list + closed_list:
                    if n.same_pos(known_node) and n > known_node:
                        break
                else:
                    heapq.heappush(open_list, n)
                    if loc in numbers:
                        distances[number][loc] = distances[loc][number] = s
            closed_list.append(node)
    return distances


def read_input(
        filename: str
        ) -> tuple[list[list[str]], dict[str, tuple[int, int]]]:
    maze = [list(line.strip()) for line in open(filename)]
    numbers = {
        maze[y][x]: (x, y)
        for y in range(len(maze))
        for x in range(len(maze[y]))
        if maze[y][x].isnumeric()
    }
    return maze, numbers


def part_one(filename: str) -> int:
    maze, numbers = read_input(filename)
    distances = find_distances(maze, numbers)
    shortest = int(1e9)
    for order in permutations([n for n in numbers if n != '0']):
        shortest = min(
            shortest,
            distances['0'][order[0]]
            + sum([distances[a][b] for a, b in pairwise(order)])
        )
    return shortest


def part_two(filename: str) -> int:
    maze, numbers = read_input(filename)
    distances = find_distances(maze, numbers)
    shortest = int(1e9)
    for order in permutations([n for n in numbers if n != '0']):
        shortest = min(
            shortest,
            distances['0'][order[0]]
            + sum([distances[a][b] for a, b in pairwise(order)])
            + distances[order[-1]]['0']
        )
    return shortest

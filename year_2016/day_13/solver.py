import heapq
from dataclasses import dataclass


@dataclass
class Node:
    x: int
    y: int
    g: int
    h: int

    def same_pos(self, other: 'Node') -> bool:
        return self.x == other.x and self.y == other.y

    def __gt__(self, other: 'Node') -> bool:
        return self.g + self.h > other.g + other.h


def is_valid(x: int, y: int, max_x: int, max_y: int, key: int) -> bool:
    return (not bool(bin(x*x + 3*x + 2*x*y + y + y*y + key).count('1') % 2)
            and 0 <= x <= max_x and 0 <= y <= max_y)


def read_input(filename: str) -> int:
    return int(open(filename).read().strip())


def part_one(filename: str) -> int:
    key, max_x, max_y = read_input(filename), 50, 50
    target = (31, 39)
    open_list = [Node(1, 1, 0, 0)]
    heapq.heapify(open_list)
    closed_list = []
    while open_list:
        node = heapq.heappop(open_list)
        next_nodes = [
            n for n in (
                (node.x+1, node.y), (node.x-1, node.y),
                (node.x, node.y+1), (node.x, node.y-1)
            )
            if is_valid(n[0], n[1], max_x, max_y, key)
        ]
        if target in next_nodes:
            return node.g + 1
        for n in next_nodes:
            new_node = Node(
                n[0], n[1],
                node.g + 1, abs(target[0] - n[0]) + abs(target[1] - n[1])
            )
            for known_node in open_list + closed_list:
                if new_node.same_pos(known_node) and new_node > known_node:
                    break
            else:
                heapq.heappush(open_list, new_node)
        closed_list.append(node)
    return -1


def part_two(filename: str) -> int:
    key, max_x, max_y = read_input(filename), 52, 52
    open_list = {(1, 1)}
    closed_list = set[tuple[int, int]]()
    for _ in range(50):
        new_open_list = set[tuple[int, int]]()
        for node in open_list:
            closed_list.add(node)
            for n in (
                    (node[0]+1, node[1]), (node[0]-1, node[1]),
                    (node[0], node[1]+1), (node[0], node[1]-1)):
                if is_valid(n[0], n[1], max_x, max_y, key):
                    new_open_list.add(n)
        open_list = new_open_list
    return len(closed_list | open_list)

import heapq
from hashlib import md5
from dataclasses import dataclass


@dataclass
class Node:
    x: int
    y: int
    g: int
    h: int
    path: str

    def same_pos(self, other: 'Node') -> bool:
        return self.x == other.x and self.y == other.y

    def __gt__(self, other: 'Node') -> bool:
        return self.g + self.h > other.g + other.h


def is_valid(x: int, y: int, c: str) -> bool:
    return 0 <= x < 4 and 0 <= y < 4 and c in "bcdef"


def read_input(filename: str):
    return open(filename).read().strip()


def search_path(passcode: str, longest: bool = False) -> str:
    open_list = [Node(0, 0, 0, 0, "")]
    heapq.heapify(open_list)
    length = 0

    while open_list:
        node = heapq.heappop(open_list)
        h = md5(f"{passcode}{node.path}".encode()).hexdigest()
        next_nodes = {
            "U": (node.x, node.y-1, h[0]),
            "D": (node.x, node.y+1, h[1]),
            "L": (node.x-1, node.y, h[2]),
            "R": (node.x+1, node.y, h[3])
        }
        for dir, n in next_nodes.items():
            if not is_valid(*n):
                continue
            if n[0] == n[1] == 3:
                if longest:
                    length = max(length, len(node.path + dir))
                    continue
                else:
                    return node.path + dir

            new_node = Node(
                n[0], n[1], node.g + 1, 6 - n[0] - n[1], node.path + dir
            )
            heapq.heappush(open_list, new_node)

    return str(length)


def part_one(filename: str) -> str:
    return search_path(read_input(filename))


def part_two(filename: str) -> str:
    return search_path(read_input(filename), longest=True)

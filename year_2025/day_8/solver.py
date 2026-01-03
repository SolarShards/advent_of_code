from math import sqrt, prod
from itertools import combinations

JunctionBox = tuple[int, int, int]


def read_input(filename: str) -> list[JunctionBox]:
    return [
        JunctionBox(map(int, line.rstrip().split(",")))
        for line in open(filename).readlines()
    ]


def distance(p1: JunctionBox, p2: JunctionBox) -> float:
    return sqrt(sum(abs(a - b)**2 for a, b in zip(p1, p2)))


def connect_pair(
        box1: JunctionBox,
        box2: JunctionBox,
        circuits: dict[int, list[JunctionBox]],
        rev_map: dict[JunctionBox, int],
        idx: int) -> int:
    if box1 in rev_map and box2 in rev_map:
        if rev_map[box1] != rev_map[box2]:
            to_merge = circuits.pop(rev_map[box2])
            for box in to_merge:
                rev_map[box] = rev_map[box1]
            circuits[rev_map[box1]] += to_merge
    elif box1 in rev_map:
        circuits[rev_map[box1]].append(box2)
        rev_map[box2] = rev_map[box1]
    elif box2 in rev_map:
        circuits[rev_map[box2]].append(box1)
        rev_map[box1] = rev_map[box2]
    else:
        circuits[idx] = [box1, box2]
        rev_map[box1] = rev_map[box2] = idx
        idx += 1
    return idx


def part_one(filename: str) -> int:
    boxes = read_input(filename)
    pairs = sorted(
        [box for box in combinations(boxes, 2)],
        key=lambda point: distance(point[0], point[1])
    )

    circuits = dict[int, list[JunctionBox]]()
    rev_map = dict[JunctionBox, int]()
    idx = 0

    for (box1, box2) in pairs[:1000]:
        idx = connect_pair(box1, box2, circuits, rev_map, idx)
    return prod(
        [len(c) for c in sorted(circuits.values(), key=len, reverse=True)[:3]]
    )


def part_two(filename: str) -> int:
    boxes = read_input(filename)
    pairs = sorted(
        [box for box in combinations(boxes, 2)],
        key=lambda point: distance(point[0], point[1])
    )

    circuits = dict[int, list[JunctionBox]]()
    rev_map = dict[JunctionBox, int]()
    idx = 0

    for (box1, box2) in pairs:
        idx = connect_pair(box1, box2, circuits, rev_map, idx)
        if len(rev_map) == len(boxes) and len(circuits) == 1:
            return box1[0] * box2[0]
    return 0

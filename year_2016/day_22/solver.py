import re
import heapq
from dataclasses import dataclass
from itertools import combinations
# import os


@dataclass
class Disk:
    size: int
    used: int
    avail: int

    def move_from(self, other: 'Disk'):
        if self.avail >= other.used:
            self.used += other.used
            self.avail -= other.used
            other.used = 0
            other.avail = other.size


@dataclass
class Node:
    x: int
    y: int
    g: int
    h: int
    disk: Disk
    previous: 'Node | None' = None

    def same_pos(self, other: 'Node') -> bool:
        return self.x == other.x and self.y == other.y

    def __gt__(self, other: 'Node') -> bool:
        return self.g + self.h >= other.g + other.h


def is_valid(
        x: int, y: int,
        target_data_x: int, target_data_y: int,
        max_x: int, max_y: int,
        last_disk: Disk,
        grid: list[list[Disk]]) -> bool:
    return (0 <= x <= max_x and 0 <= y <= max_y
            and (x != target_data_x or y != target_data_y)
            and grid[y][x].used <= last_disk.size)


def read_input(filename: str):
    pattern = re.compile(r"\/dev\/grid\/node-x(\d+)-y(\d+)")
    lines = [line.split() for line in open(filename)]
    max_x, max_y = 0, 0
    if (m := re.match(pattern, lines[-1][0])):
        max_x, max_y = (int(g) for g in m.groups())
    grid = [[Disk(0, 0, 0) for x in range(max_x+1)] for x in range(max_y+1)]
    for line in lines:
        if (m := re.match(pattern, line[0])):
            grid[int(m.group(2))][int(m.group(1))] = \
                Disk(*(int(s[:-1]) for s in line[1:-1]))

    return grid


def part_one(filename: str) -> int:
    grid = read_input(filename)
    return sum([
        (0 < a.used <= b.avail) or (0 < b.used <= a.avail)
        for a, b in combinations([node for row in grid for node in row], 2)
    ])


def part_two(filename: str) -> int:
    grid = read_input(filename)
    # define goal data's disk position
    goal_data_pos = (len(grid[0])-1, 0)

    # find empty disk's position
    empty_disk = (100, 100)
    empty_disk_found = False
    for y in range(len(grid)):
        if empty_disk_found:
            break
        for x in range(len(grid[0])):
            if grid[y][x].used == 0:
                empty_disk = (x, y)
                empty_disk_found = True
                break

    steps = 0
    while goal_data_pos != (0, 0):

        # define the node on the left of the goal data's node as the A* target
        target = (goal_data_pos[0]-1, 0)

        # create open and closed lists
        open_list = [
            Node(*empty_disk, 0, 0, grid[empty_disk[1]][empty_disk[0]])
        ]
        heapq.heapify(open_list)
        closed_list: list[Node] = []

        # execute A* algorithm
        while open_list:

            # find valid disks around the current best node
            node = heapq.heappop(open_list)
            next_nodes = [
                n for n in (
                    (node.x+1, node.y), (node.x-1, node.y),
                    (node.x, node.y+1), (node.x, node.y-1)
                )
                if is_valid(
                    n[0], n[1],
                    *goal_data_pos,
                    len(grid[0])-1, len(grid)-1,
                    node.disk, grid
                )
            ]

            # Uncomment to see A* work step by step
            """ os.system('cls')
            for y in range(len(grid)):
                print(" ".join(
                    "G" if (x, y) == goal_data_pos
                    else "_" if grid[y][x].used == 0
                    else "X" if (x, y) in next_nodes
                    else "#" if (x, y) in [(n.x, n.y) for n in closed_list]
                    else "."
                    for x in range(len(grid[y]))))
            input() """

            # move data and count steps if the target is reached
            # from the empty node
            if target in next_nodes:
                # move data to make the disk before the target empty
                path = [node]
                while path[0].previous:
                    path.insert(0, path[0].previous)
                for n in path[1:]:
                    if n.previous:
                        n.previous.disk.move_from(n.disk)
                # empty the target disk in the previous disk
                node.disk.move_from(grid[target[1]][target[0]])
                # move goal data in the target disk
                grid[target[1]][target[0]].move_from(
                    grid[goal_data_pos[1]][goal_data_pos[0]]
                )
                # add steps to epmty the target + the step to move goal data
                steps += len(path) + 1
                # set the coordinates of the disk that now contains goal data
                empty_disk = goal_data_pos
                goal_data_pos = target
                # end of A* algorithm
                break

            # create new nodes and add them to open list if they are valuable
            for n in next_nodes:
                # Customized Manhattan heuristic:
                # If a wall is blocking the view from the target,
                # Going away from the wall has a tremendous cost
                # Set h_xf and h_yf to 1 to have classical Manhattan
                opp_x, opp_y = 2 * node.x - n[0], 2 * node.y - n[1]
                h_xf = 500 if 0 <= opp_x < len(grid[0]) \
                    and grid[n[1]][opp_x].used > 100 else 1
                h_yf = 500 if 0 <= opp_y < len(grid) \
                    and grid[opp_y][n[0]].used > 100 else 1

                new_node = Node(
                    n[0], n[1],
                    node.g + 1,
                    h_xf*abs(target[0] - n[0]) + h_yf*abs(target[1] - n[1]),
                    grid[n[1]][n[0]], node
                )
                for known_node in open_list + closed_list:
                    if new_node.same_pos(known_node) and new_node > known_node:
                        break
                else:
                    heapq.heappush(open_list, new_node)
            # add the current node to the closed list
            closed_list.append(node)
    return steps

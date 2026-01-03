from itertools import combinations, pairwise
from multiprocessing import Process, Queue, cpu_count, Barrier as mp_barrier
from threading import Barrier


def read_input(filename: str) -> list[tuple[int, int]]:
    return [
        tuple[int, int](map(int, line.rstrip().split(",")))
        for line in open(filename).readlines()
    ]


def surface(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def part_one(filename: str) -> int:
    return max(
        [surface(*pair) for pair in combinations(read_input(filename), 2)]
    )


def check_rectangle(
        pairs: list[tuple[tuple[int, int], tuple[int, int]]],
        borders: list[tuple[int, int]],
        start: int,
        step: int,
        queue: Queue,
        barrier: Barrier
        ):

    for t0, t1 in pairs[start::step]:
        barrier.wait()
        x0, x1 = (t0[0], t1[0]) if t0[0] < t1[0] else (t1[0], t0[0])
        y0, y1 = (t0[1], t1[1]) if t0[1] < t1[1] else (t1[1], t0[1])
        for tile in borders:
            if (x0) < tile[0] < x1 and y0 < tile[1] < y1:
                break
        else:
            queue.put(surface(t0, t1))
            return


def part_two(filename: str) -> int:
    tiles = read_input(filename)
    queue = Queue(1)
    barrier = mp_barrier(cpu_count())

    borders = list[tuple[int, int]]()
    for t0, t1 in pairwise(tiles + [tiles[0]]):
        if t0[0] == t1[0]:
            borders += [
                (t0[0], y)
                for y in range(min(t0[1], t1[1]), max(t0[1], t1[1]))
            ]
        else:
            borders += [
                (x, t0[1])
                for x in range(min(t0[0], t1[0]), max(t0[0], t1[0]))
            ]

    pairs = sorted(
        [p for p in combinations(tiles, 2)],
        key=lambda pair: surface(*pair),
        reverse=True
    )

    processes = [
        Process(
            target=check_rectangle,
            args=(pairs, borders, start_value, cpu_count(), queue, barrier)
        )
        for start_value in range(cpu_count())
    ]

    for process in processes:
        process.start()

    result = queue.get()

    for process in processes:
        process.kill()

    return result

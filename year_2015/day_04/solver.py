from multiprocessing import Process, Queue, cpu_count, Barrier as mp_barrier
from threading import Barrier
from hashlib import md5


def read_input(_: str) -> str:
    return "bgvyzdsv"


def hash_process(
        input_string: str,
        prefix: str,
        start: int,
        step: int,
        queue: Queue,
        barrier: Barrier):
    h = ""
    test_val = start - step
    while not h.startswith(prefix):
        barrier.wait()
        test_val += step
        h = md5(f"{input_string}{test_val}".encode()).hexdigest()
    queue.put(test_val)


def find_hash(input_string: str, difficulty: int):
    queue = Queue(1)
    barrier = mp_barrier(cpu_count())
    prefix = "0" * difficulty

    hash_cores = [
        Process(
            target=hash_process,
            args=(
                input_string, prefix, start_value, cpu_count(), queue, barrier
            )
        )
        for start_value in range(cpu_count())
    ]

    for process in hash_cores:
        process.start()

    print(f"Searching hash on {cpu_count()} cores")
    result = queue.get()

    for process in hash_cores:
        process.kill()

    return result


def part_one(_: str) -> int:
    return find_hash(read_input(""), 5)


def part_two(_: str) -> int:
    return find_hash(read_input(""), 6)

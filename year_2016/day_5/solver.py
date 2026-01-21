from multiprocessing import Process, Queue, cpu_count
from hashlib import md5


def read_input(_: str) -> str:
    return "ugkcyxxp"


def hash_process(
        input_string: str,
        prefix: str,
        hash_queue: Queue,
        chunk_queue: Queue):
    while True:
        start, end = chunk_queue.get()
        for test_val in range(start, end):
            h = md5(f"{input_string}{test_val}".encode()).hexdigest()
            if h.startswith(prefix):
                hash_queue.put((test_val, h))


def find_hashes(
        input_string: str,
        part: int,
        difficulty: int,
        chunk_size: int) -> dict[int, str]:

    prefix = "0" * difficulty
    hash_queue = Queue(8 if part == 1 else 1)

    chunk_queue = Queue(cpu_count())
    chunk_start, chunk_end = 0, chunk_size
    while not chunk_queue.full():
        chunk_queue.put((chunk_start, chunk_end))
        chunk_start, chunk_end = chunk_end, chunk_end + chunk_size

    hash_cores = [
        Process(
            target=hash_process,
            args=(
                input_string, prefix, hash_queue, chunk_queue
            )
        )
        for _ in range(cpu_count())
    ]

    for process in hash_cores:
        process.start()

    print(f"Searching hash on {cpu_count()} cores")
    hashes: dict[int, str] = {}

    while True:
        while hash_queue.empty():
            while not chunk_queue.full():
                chunk_queue.put((chunk_start, chunk_end))
                chunk_start, chunk_end = chunk_end, chunk_end + chunk_size

        hash = hash_queue.get()[1]

        if part == 1:
            hashes[len(hashes)] = hash
            print(f"Found hash {len(hashes)-1}: {hashes[len(hashes)-1]}")

        else:
            idx = int(hash[5], 16)
            if idx in range(8) and idx not in hashes:
                hashes[idx] = hash
                print(f"Found hash {idx}: {hash}")

        if len(hashes) == 8:
            break

    for process in hash_cores:
        process.kill()

    return hashes


def part_one(_: str) -> str:
    return "".join([
        hash[5] for hash in find_hashes(read_input(_), 1, 5, 1000).values()
    ])


def part_two(_: str) -> str:
    hashes = find_hashes(read_input(_), 2, 5, 1000)
    return "".join(
        hashes[i][6] for i in range(8)
    )

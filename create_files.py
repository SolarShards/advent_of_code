import os
import sys

template = """def read_input(filename: str):
    return


def part_one(filename: str) -> int:
    return 0


def part_two(filename: str) -> int:
    return 0


if __name__ == "__main__":
    import os
    print(read_input(os.path.dirname(__file__) + "/input.txt"))
    print(part_one(os.path.dirname(__file__) + "/input.txt"))
    print(part_two(os.path.dirname(__file__) + "/input.txt"))
"""

os.mkdir(f"{os.path.dirname(__file__)}/year_{sys.argv[1]}")
for day in range(1, 26):
    path = f"{os.path.dirname(__file__)}/year_{sys.argv[1]}/day_{day}"
    os.mkdir(path)
    with open(f"{path}/input.txt", "w") as f:
        pass
    with open(f"{path}/solver.py", "w") as f:
        f.write(template)

import json
from typing import Any


def read_input(filename: str) -> dict[str, Any]:
    return json.load(open(filename))


def sum_content(obj: Any, filter: Any = None) -> int:
    if isinstance(obj, dict):
        if filter in obj.values():
            return 0
        else:
            return sum(sum_content(v, filter) for v in obj.values())
    elif isinstance(obj, list):
        return sum(sum_content(v, filter) for v in obj)
    elif isinstance(obj, int):
        return obj
    else:
        return 0


def part_one(filename: str) -> int:
    return sum_content(read_input(filename))


def part_two(filename: str) -> int:
    return sum_content(read_input(filename), filter="red")


if __name__ == "__main__":
    import os
    print(part_one(os.path.dirname(__file__) + "\\input.txt"))
    print(part_two(os.path.dirname(__file__) + "\\input.txt"))

import os
import importlib
import argparse
import time
from typing import Callable
from multiprocessing import freeze_support


def profile(function: Callable, *args):
    start_clock_time = time.perf_counter_ns()
    start_cpu_time = time.process_time_ns()

    ret = function(*args)

    end_clock_time = time.perf_counter_ns()
    end_cpu_time = time.process_time_ns()

    print(f"\nProfiling of {function.__name__}:")
    print(f"    Clock time: {(end_clock_time - start_clock_time) / 1e9} s")
    print(f"      CPU time: {(end_cpu_time - start_cpu_time) / 1e9} s\n")

    return ret


def execute(y: str, days: list[str]):
    for d in days:
        try:
            mod = importlib.import_module(f"{y}.{d}.solver")
        except ModuleNotFoundError:
            exit()
        print("-----------------------------------------------------")
        print(f"Day {d}:")
        print(f"Part one result:{profile(mod.part_one, f"{y}/{d}/input.txt")}")
        print(f"Part two result:{profile(mod.part_two, f"{y}/{d}/input.txt")}")
        print("-----------------------------------------------------")


if __name__ == "__main__":
    freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--day", type=int, help="Executes only this day if given"
    )
    parser.add_argument(
        "-y", "--year", type=int,
        help="Executes this year if given, else executes latest."
    )
    args = parser.parse_args()

    year = args.year if args.year else "year_" + str(max([
        int(dir[5:])
        for dir in os.listdir(os.path.dirname(__file__))
        if dir[5:].isnumeric()
    ]))

    days = [
        args.day if args.day else dir
        for dir in os.listdir(os.path.dirname(__file__) + f"/{year}")
    ]

    execute(year, days)

import os
import importlib
import argparse
import time
import subprocess
from typing import Callable
from multiprocessing import freeze_support


def profile(function: Callable, *args, label: str | None = None):
    start_clock_time = time.perf_counter_ns()
    start_cpu_time = time.process_time_ns()

    ret = function(*args)

    end_clock_time = time.perf_counter_ns()
    end_cpu_time = time.process_time_ns()

    name = label if label else function.__name__
    print(f"\nProfiling of {name}:")
    print(f"    Clock time: {(end_clock_time - start_clock_time) / 1e9} s")
    print(f"      CPU time: {(end_cpu_time - start_cpu_time) / 1e9} s\n")

    return ret


def run_cpp_part(exe_path: str, day_path: str, part: int) -> str:
    proc = subprocess.run([exe_path, str(part)], cwd=os.path.dirname(exe_path), capture_output=True, text=True)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, [exe_path, str(part)], output=proc.stdout, stderr=proc.stderr)
    return proc.stdout.strip()


def execute(y: str, days: list[str]):
    # If a top-level CMakeLists.txt exists for the year, configure and build it once
    year_dir = os.path.join(os.path.dirname(__file__), y)
    year_cmake = os.path.join(year_dir, 'CMakeLists.txt')
    year_build_dir = os.path.join(year_dir, 'build')
    use_year_cmake = os.path.exists(year_cmake)
    year_target = None
    if use_year_cmake:
        os.makedirs(year_build_dir, exist_ok=True)
        try:
            print("Configuring year-level CMake...")
            subprocess.run(["cmake", ".."], cwd=year_build_dir, check=True)
            # If a single day is requested, build only that target to save time
            if len(days) == 1:
                year_target = days[0].replace("_", "")
                print(f"Building year-level target {year_target}...")
                subprocess.run(["cmake", "--build", ".", "--target", year_target, "--parallel"], cwd=year_build_dir, check=True)
                print("Year-level CMake build complete for target.")
            else:
                print("Year-level CMake configured (not building all targets).")
        except subprocess.CalledProcessError as e:
            print(f"Year-level CMake/build failed: {e}")
            use_year_cmake = False

    for d in days:
        day_path = os.path.join(year_dir, d)
        # Try Python solver first
        try:
            mod = importlib.import_module(f"{y}.{d}.solver")
        except ModuleNotFoundError:
            mod = None

        print("-----------------------------------------------------")
        print(f"Day {d}:")

        if mod is not None:
            print(f"Part one result: {profile(mod.part_one, f"{y}/{d}/input.txt")}")
            print(f"Part two result: {profile(mod.part_two, f"{y}/{d}/input.txt")}")
            print("-----------------------------------------------------")
            continue

        # If year-level CMake was used, look for the expected executable in the day source folder
        if use_year_cmake:
            exe_dir = day_path
            exe_path = None
            if year_target is not None:
                candidate = os.path.join(day_path, year_target)
                if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                    exe_path = candidate

            if exe_path is None and os.path.isdir(exe_dir):
                for root, _, files in os.walk(exe_dir):
                    for f in files:
                        p = os.path.join(root, f)
                        if os.path.isfile(p) and os.access(p, os.X_OK):
                            exe_path = p
                            break
                    if exe_path:
                        break

            if exe_path:
                try:
                    print(f"Part one result: {profile(run_cpp_part, exe_path, day_path, 1, label='Part 1')}")
                    print(f"Part two result: {profile(run_cpp_part, exe_path, day_path, 2, label='Part 2')}")
                except subprocess.CalledProcessError as e:
                    print(f"  C++ execution failed: {e}\n{e.stderr}")
                except Exception as e:
                    print(f"  Failed to run executable: {e}")
                print("-----------------------------------------------------")
                continue
            else:
                print(f"  No executable found for {d} in year-level build")

        # Fallback: per-day CMake or sources
        try:
            entries = os.listdir(day_path)
        except FileNotFoundError:
            print(f"  No solver found for {d} (missing directory)")
            print("-----------------------------------------------------")
            continue

        is_cpp = any(name.endswith(('.cpp', '.cc', '.cxx')) for name in entries) or 'CMakeLists.txt' in entries
        if not is_cpp:
            print(f"  No Python or C++ solver found for {d}")
            print("-----------------------------------------------------")
            continue

        build_dir = os.path.join(day_path, 'build')
        os.makedirs(build_dir, exist_ok=True)

        try:
            print("  Configuring CMake...")
            subprocess.run(["cmake", ".."], cwd=build_dir, check=True)
            print("  Building C++ project...")
            subprocess.run(["cmake", "--build", ".", "--parallel"], cwd=build_dir, check=True)

            # find first executable in build dir
            exe_path = None
            for root, _, files in os.walk(build_dir):
                for f in files:
                    p = os.path.join(root, f)
                    if os.path.isfile(p) and os.access(p, os.X_OK):
                        exe_path = p
                        break
                if exe_path:
                    break

            if not exe_path:
                print("  Build finished but no executable found in build/")
                print("-----------------------------------------------------")
                continue

            try:
                print(f"Part one result: {profile(run_cpp_part, exe_path, day_path, 1)}")
                print(f"Part two result: {profile(run_cpp_part, exe_path, day_path, 2)}")
            except subprocess.CalledProcessError as e:
                print(f"  C++ execution failed: {e}\n{e.stderr}")
            except Exception as e:
                print(f"  Failed to run executable: {e}")
        except subprocess.CalledProcessError as e:
            print(f"  CMake/build failed: {e}")
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

    year = f"year_{args.year}" if args.year else str(max([
        int(dir[5:])
        for dir in os.listdir(os.path.dirname(__file__))
        if dir[5:].isnumeric()
    ]))
    print(year)

    if args.day:
        days = [f"day_{args.day}"]
    else:
        year_dir = os.path.dirname(__file__) + f"/{year}"
        days = [
            dir for dir in os.listdir(year_dir)
            if os.path.isdir(os.path.join(year_dir, dir)) and dir.startswith("day_")
        ]
        days.sort(key=lambda x: int(x.split("_")[1]))
    print(days)

    execute(year, days)

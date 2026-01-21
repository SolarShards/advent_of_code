import re


class Scrambler:

    def __init__(self, instructions: list[str]):
        self.__instructions = instructions
        self.__op_map = {
            r"swap position (\d+) with position (\d+)": self.__swap_position,
            r"swap letter (.) with letter (.)": self.__swap_letters,
            r"rotate (left|right) (\d+) steps?": self.__rotate_n,
            r"rotate based on position of letter (.)": self.__rotate_from_pos,
            r"reverse positions (\d+) through (\d+)": self.__reverse,
            r"move position (\d+) to position (\d+)": self.__move
        }
        self.__operations = [
            (
                operation,
                tuple(int(g) if g.isnumeric() else g for g in m.groups())
             )
            for inst in self.__instructions
            for pattern, operation in self.__op_map.items()
            if (m := re.match(pattern, inst))
        ]

    def scramble(self, string: str) -> str:
        self.__string = list(string)
        self.__rot_map = {
            i: -(i + 1 + (i >= 4))
            for i in range(len(string))
        }
        steps = ["".join(self.__string) + '\n']
        for op, params in self.__operations:
            op(*params, False)
            steps.append("".join(self.__string) + '\n')
        with open("scrambling.txt", 'w') as f:
            f.writelines(steps)
        return "".join(self.__string)

    def unscramble(self, string: str) -> str:
        self.__string = list(string)
        self.__rot_map = {
            (2 * i + 1 + (i >= 4)) % len(string): i + 1 + (i >= 4)
            for i in range(len(string))
        }
        steps = ["".join(self.__string) + '\n']
        for op, params in reversed(self.__operations):
            op(*params, True)
            steps.append("".join(self.__string) + '\n')
        with open("unscrambling.txt", 'w') as f:
            f.writelines(reversed(steps))
        return "".join(self.__string)

    def __swap_position(
            self,
            x: int,
            y: int,
            _: bool = False):
        self.__string[x], self.__string[y] = self.__string[y], self.__string[x]

    def __swap_letters(
            self,
            x: str,
            y: str,
            _: bool = False):
        ix, iy = self.__string.index(x), self.__string.index(y)
        self.__string[ix], self.__string[iy] = y, x

    def __rotate_n(
            self,
            direction: str,
            steps: int,
            rev: bool = False):
        if (direction, rev) in (("right", False), ("left", True)):
            steps = (-steps)
        steps %= len(self.__string)
        self.__string = self.__string[steps:] + self.__string[:steps]

    def __rotate_from_pos(
            self,
            letter: str,
            _: bool = False):
        idx = self.__rot_map[self.__string.index(letter)] % len(self.__string)
        self.__string = self.__string[idx:] + self.__string[:idx]

    def __reverse(
            self,
            x: int,
            y: int,
            _: bool):
        self.__string = self.__string[:x] \
            + self.__string[x:y+1][::-1] + self.__string[y+1:]

    def __move(
            self,
            x: int,
            y: int,
            rev: bool = False):
        c = self.__string.pop(y if rev else x)
        self.__string.insert(x if rev else y, c)


def read_input(filename: str) -> list[str]:
    return [line.strip() for line in open(filename)]


def part_one(filename: str) -> str:
    return Scrambler(read_input(filename)).scramble("abcdefgh")


def part_two(filename: str) -> str:
    return Scrambler(read_input(filename)).unscramble("fbgdceah")

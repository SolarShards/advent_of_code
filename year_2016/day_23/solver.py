import re


class Computer:

    ADD_PATTERN = re.compile(
        r"(?:inc (.+)\ndec (.+)\njnz \2 -2\n)|(?:dec (.+)\ninc (.+)\njnz \3 -2\n)")  # noqa

    MUL_PATTERN = re.compile(
        r"(?:inc (.+)\ndec (.+)\njnz \2 -2\ndec (.+)\njnz \3 -5\n)|(?:dec (.+)\ninc (.+)\njnz \4 -2\ndec (.+)\njnz \6 -5\n)")  # noqa

    @staticmethod
    def optimize_addition(m: re.Match[str]) -> str:
        g = m.groups()
        dest, to_add = g[:2] if g[0] is not None else g[2:][::-1]
        return f"add {to_add} {dest}\nnop\nnop\n"

    @staticmethod
    def optimize_multiplication(m: re.Match[str]) -> str:
        g = m.groups()
        dest, lhs, rhs = g[:3] if g[0] is not None else g[3:]
        return f"mul {lhs} {rhs} {dest}\nnop\nnop\nnop\nnop\n"

    @staticmethod
    def optimize_program(program: str) -> list[tuple[str, ...]]:
        program = re.sub(
            Computer.MUL_PATTERN,
            Computer.optimize_multiplication,
            program
        )
        program = re.sub(
            Computer.ADD_PATTERN,
            Computer.optimize_addition,
            program
        )
        return [tuple(line.split()) for line in program.split("\n")]

    def __init__(self):
        self.registers = {c: 0 for c in "abcd"}
        self._pc = 0
        self._initial_program = ""
        self._program: list[tuple[str, ...]] = []
        self._instruction_set = {
            "cpy": self.cpy,
            "inc": self.inc,
            "dec": self.dec,
            "jnz": self.jnz,
            "tgl": self.tgl,
            "add": self.add,
            "mul": self.mul,
            "nop": self.nop
        }
        self._tgl_map = {
            "cpy": "jnz",
            "inc": "dec",
            "dec": "inc",
            "jnz": "cpy",
            "tgl": "inc"
        }

    def nop(self):
        self._pc += 1

    def cpy(self, value: str, dest: str):
        if dest in self.registers:
            if value in self.registers:
                self.registers[dest] = self.registers[value]
            else:
                self.registers[dest] = int(value)
        self._pc += 1

    def inc(self, register: str):
        if register in self.registers:
            self.registers[register] += 1
        self._pc += 1

    def dec(self, register: str):
        if register in self.registers:
            self.registers[register] -= 1
        self._pc += 1

    def add(self, to_add: str, dest: str):
        self.registers[dest] += self.registers[to_add]
        self.registers[to_add] = 0
        self._pc += 1

    def mul(self, lhs: str, rhs: str, dest: str):
        self.registers[dest] = self.registers[lhs] * self.registers[rhs]
        self.registers[lhs] = self.registers[rhs] = 0
        self._pc += 1

    def jnz(self, value: str, offset: str):
        v = self.registers[value] if value in self.registers else value
        o = self.registers[offset] if offset in self.registers else offset
        self._pc += int(o) if v else 1

    def tgl(self, value: str):
        program = self._raw_program.split("\n")
        addr = self._pc
        if value in self.registers:
            addr += self.registers[value]
        else:
            addr += int(value)
        if 0 <= addr < len(program):
            instruction, arguments = program[addr].split(" ", 1)
            program[addr] = self._tgl_map[instruction] + " " + arguments
            self._raw_program = "\n".join(program)
            self._program = Computer.optimize_program(self._raw_program)
        self._pc += 1

    def run_program(self, program: str):
        self._raw_program = program
        self._program = Computer.optimize_program(program)
        while 0 <= self._pc < len(self._program):
            instruction = self._program[self._pc][0]
            arguments = self._program[self._pc][1:]
            self._instruction_set[instruction](*arguments)


def read_input(filename: str) -> str:
    return open(filename).read()


def part_one(filename: str) -> int:
    computer = Computer()
    computer.registers['a'] = 7
    computer.run_program(read_input(filename))
    return computer.registers['a']


def part_two(filename: str) -> int:
    computer = Computer()
    computer.registers['a'] = 12
    computer.run_program(read_input(filename))
    return computer.registers['a']

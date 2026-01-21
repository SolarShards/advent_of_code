class Computer:

    def __init__(self):
        self.registers = {c: 0 for c in "abcd"}
        self._pc = 0
        self._program: list[tuple[str, ...]] = []
        self._instruction_set = {
            "cpy": self.cpy,
            "inc": self.inc,
            "dec": self.dec,
            "jnz": self.jnz
        }

    def cpy(self, value: str, dest: str):
        if value.isnumeric():
            self.registers[dest] = int(value)
        else:
            self.registers[dest] = self.registers[value]
        self._pc += 1

    def inc(self, register: str):
        self.registers[register] += 1
        self._pc += 1

    def dec(self, register: str):
        self.registers[register] -= 1
        self._pc += 1

    def jnz(self, value: str, offset: int):
        if value.isnumeric():
            self._pc += int(offset) if int(value) else 1
        else:
            self._pc += int(offset) if self.registers.get(value) else 1

    def run_program(self, program: list[tuple[str, ...]]):
        self._program = program
        while 0 <= self._pc < len(self._program):
            instruction = self._program[self._pc][0]
            arguments = self._program[self._pc][1:]
            self._instruction_set[instruction](*arguments)


def read_input(filename: str):
    return [tuple(line.split()) for line in open(filename)]


def part_one(filename: str) -> int:
    computer = Computer()
    computer.run_program(read_input(filename))
    return computer.registers['a']


def part_two(filename: str) -> int:
    computer = Computer()
    computer.registers['c'] = 1
    computer.run_program(read_input(filename))
    return computer.registers['a']

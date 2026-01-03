class Computer:

    def __init__(self):
        self.registers = {'a': 0, 'b': 0}
        self._pc = 0
        self._program: list[tuple[str, ...]] = []
        self._instruction_set = {
            "hlf": self.hlf,
            "tpl": self.tpl,
            "inc": self.inc,
            "jmp": self.jmp,
            "jie": self.jie,
            "jio": self.jio,
        }

    def hlf(self, register: str):
        self.registers[register] //= 2
        self._pc += 1

    def tpl(self, register: str):
        self.registers[register] *= 3
        self._pc += 1

    def inc(self, register: str):
        self.registers[register] += 1
        self._pc += 1

    def jmp(self, offset: str):
        self._pc += int(offset)

    def jie(self, register: str, offset: str):
        self._pc += int(offset) if not self.registers[register[0]] % 2 else 1

    def jio(self, register: str, offset: str):
        self._pc += int(offset) if self.registers[register[0]] == 1 else 1

    def run_program(self, program: list[tuple[str, ...]]):
        self._program = program
        while 0 <= self._pc < len(self._program):
            instruction = self._program[self._pc][0]
            arguments = self._program[self._pc][1:]
            self._instruction_set[instruction](*arguments)


def read_input(filename: str) -> list[tuple[str, ...]]:
    return [tuple(line.split()) for line in open(filename)]


def part_one(filename: str) -> int:
    computer = Computer()
    computer.run_program(read_input(filename))
    return computer.registers['b']


def part_two(filename: str) -> int:
    computer = Computer()
    computer.registers['a'] = 1
    computer.run_program(read_input(filename))
    return computer.registers['b']

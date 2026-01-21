class Computer:

    def __init__(self):
        self.registers = {c: 0 for c in "abcd"}
        self._pc = 0
        self._program: list[tuple[str, ...]] = []
        self._output = [2]
        self._instruction_set = {
            "cpy": self.cpy,
            "inc": self.inc,
            "dec": self.dec,
            "jnz": self.jnz,
            "out": self.out
        }

    def out(self, value: str):
        if value in self.registers:
            self._output.append(self.registers[value])
        else:
            self._output.append(int(value))
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

    def jnz(self, value: str, offset: str):
        v = self.registers[value] if value in self.registers else value
        o = self.registers[offset] if offset in self.registers else offset
        self._pc += int(o) if int(v) else 1

    def calibrate(self, program: str) -> int:
        self._program = [tuple(line.split()) for line in program.split("\n")]
        a = -1
        while True:
            self._pc = 0
            a += 1
            self.registers['a'], self._output = a, []
            while 0 <= self._pc < len(self._program):
                instruction = self._program[self._pc][0]
                arguments = self._program[self._pc][1:]
                self._instruction_set[instruction](*arguments)
                if instruction == "out" and len(self._output) >= 10:
                    if self._output in ([0, 1]*5, [1, 0]*5):
                        return a
                    else:
                        break


def read_input(filename: str) -> str:
    return open(filename).read()


def part_one(filename: str) -> int:
    computer = Computer()
    return computer.calibrate(read_input(filename))


def part_two(filename: str) -> int:
    return 0

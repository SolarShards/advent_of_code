from copy import deepcopy

gates = {
    "EQ": lambda op1, op2: op1,
    "OR": lambda op1, op2: op1 | op2,
    "AND": lambda op1, op2: op1 & op2,
    "NOT": lambda op1, op2: ~op1 & 0xFFFF,
    "LSHIFT": lambda op1, op2: op1 << op2,
    "RSHIFT": lambda op1, op2: op1 >> op2
}


def read_input(
        filename: str
        ) -> dict[str, tuple[
                str | int,  # Operand 1
                str,  # Operation
                str | int | None,  # Operand 2
            ]]:
    instructions = {}
    for ins in [line.split() for line in open(filename)]:
        lhs = ins[:-2]
        op1, gate, op2 = "", "", None
        if len(lhs) == 1:
            op1 = int(lhs[0]) if lhs[0].isnumeric() else lhs[0]
            gate = "EQ"
        elif len(lhs) == 2:
            op1 = int(lhs[1]) if lhs[1].isnumeric() else lhs[1]
            gate = "NOT"
        else:
            op1 = int(lhs[0]) if lhs[0].isnumeric() else lhs[0]
            gate = lhs[1]
            op2 = int(lhs[2]) if lhs[2].isnumeric() else lhs[2]
        instructions[ins[-1]] = (op1, gate, op2)
    return instructions


def connect_circuit(
        circuit: dict[str, tuple[str | int, str, str | int | None]]
        ) -> dict[str, int]:
    values: dict[str, int] = {}
    while circuit:
        closed_list = []
        for out, (op1, gate, op2) in circuit.items():
            op1 = values.get(op1, op1)  # type: ignore
            op2 = values.get(op2, op2)  # type: ignore
            if type(op1) is int and type(op2) in (int, type(None)):
                values[out] = gates[gate](op1, op2)
                closed_list.append(out)
        for out in closed_list:
            del circuit[out]
    return values


def part_one(filename: str) -> int:
    return connect_circuit(read_input(filename))["a"]


def part_two(filename: str) -> int:
    circuit = read_input(filename)
    b = circuit['b']
    circuit["b"] = (
        connect_circuit(deepcopy(circuit))["a"], b[1], b[2]
    )
    return connect_circuit(circuit)["a"]


if __name__ == "__main__":
    import os
    print(part_two(os.path.dirname(__file__) + "\\input.txt"))

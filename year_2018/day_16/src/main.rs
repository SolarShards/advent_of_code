use std::{env, fs};
use std::collections::HashMap;
use regex::Regex;

#[derive(PartialEq, Clone, Copy)]
struct Registers([i32; 4]);
#[derive(PartialEq, Clone, Copy)]
struct Instruction([i32; 4]);
type Program = Vec<Instruction>;
struct Computer {
    registers: Registers
}

impl Computer {
    const INSTRUCTION_SET: [(&str, fn(&mut Computer, i32, i32, i32)); 16] = [
        ("addr", Computer::addr),
        ("addi", Computer::addi),
        ("mulr", Computer::mulr),
        ("muli", Computer::muli),
        ("banr", Computer::banr),
        ("bani", Computer::bani),
        ("borr", Computer::borr),
        ("bori", Computer::bori),
        ("setr", Computer::setr),
        ("seti", Computer::seti),
        ("gtir", Computer::gtir),
        ("gtri", Computer::gtri),
        ("gtrr", Computer::gtrr),
        ("eqir", Computer::eqir),
        ("eqri", Computer::eqri),
        ("eqrr", Computer::eqrr)
    ];

    fn new() -> Computer {
        Computer { registers: Registers([0; 4]) }
    }

    fn register(&mut self, reg: i32) -> &mut i32 {
        &mut self.registers.0[reg as usize]
    }

    fn addr(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = *self.register(a) + *self.register(b);
    }

    fn addi(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = *self.register(a) + b;
    }

    fn mulr(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = *self.register(a) * *self.register(b);
    }

    fn muli(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = *self.register(a) * b;
    }

    fn banr(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = *self.register(a) & *self.register(b);
    }

    fn bani(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = *self.register(a) & b;
    }

    fn borr(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = *self.register(a) | *self.register(b);
    }

    fn bori(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = *self.register(a) | b;
    }

    fn setr(&mut self, a: i32, _: i32, c: i32) {
        *self.register(c) = *self.register(a);
    }

    fn seti(&mut self, a: i32, _: i32, c: i32) {
        *self.register(c) = a;
    }

    fn gtir(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = (a > *self.register(b)) as i32;
    }

    fn gtri(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = (*self.register(a) > b) as i32;
    }

    fn gtrr(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = (*self.register(a) > *self.register(b)) as i32;
    }

    fn eqir(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = (a == *self.register(b)) as i32;
    }

    fn eqri(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = (*self.register(a) == b) as i32;
    }

    fn eqrr(&mut self, a: i32, b: i32, c: i32) {
        *self.register(c) = (*self.register(a) == *self.register(b)) as i32;
    }
}


#[derive(PartialEq, Clone, Copy)]
struct Sample {
    input: Registers,
    instruction: Instruction,
    output: Registers
}

impl Sample {
    fn potential_opcodes(&self) -> Vec<&str> {
        let mut valid_opcodes = Vec::new();
        let mut computer = Computer::new();
        let [a, b, c] = self.instruction.0[1..] else { panic!() };
        for (name, opcode) in Computer::INSTRUCTION_SET {
            computer.registers = self.input;
            opcode(&mut computer, a, b, c);
            if computer.registers == self.output {
                valid_opcodes.push(name);
            }
        }
        valid_opcodes
    }
}

fn read_input(filename: &str) -> (Vec<Sample>, Program) {
    let mut samples: Vec<Sample> = Vec::new();
    let mut program: Program = Program::new();

    let file: String = fs::read_to_string(filename).unwrap();
    let (s, p) = file.split_once("\n\n\n").unwrap();

    let samples_re: Regex = Regex::new(
        r"Before: \[(\d+), (\d+), (\d+), (\d+)\]\n(\d+) (\d+) (\d+) (\d+)\nAfter:  \[(\d+), (\d+), (\d+), (\d+)\]"
    ).unwrap();

    samples_re.captures_iter(s).for_each(|caps| {
        let tokens: [i32; 12] = caps.extract().1.map(|x| x.parse::<i32>().unwrap());
        samples.push(Sample {
            input: Registers(tokens[0..4].try_into().unwrap()),
            instruction: Instruction(tokens[4..8].try_into().unwrap()),
            output: Registers(tokens[8..12].try_into().unwrap()) });
    });

    let program_re: Regex = Regex::new(r"(\d+) (\d+) (\d+) (\d+)").unwrap();

    program_re.captures_iter(p).for_each(|caps| {
        let tokens: [i32; 4] = caps.extract().1.map(|x| x.parse::<i32>().unwrap());
        program.push(Instruction(tokens));
    });

    (samples, program)
}

fn part_one(samples: Vec<Sample>) -> u32 {
    samples.iter().filter(|&s| s.potential_opcodes().len() >= 3).count() as u32
}

fn part_two(samples: Vec<Sample>, program: Program) -> i32 {
    let mut stats = (0..16)
        .map(|opcode| {
            (
                opcode,
                Computer::INSTRUCTION_SET
                    .iter()
                    .map(|&(name, _)| (name, 0u32))
                    .collect::<HashMap<&str, u32>>()
            )
        })
        .collect::<HashMap<i32, HashMap<&str, u32>>>();

    samples
        .iter()
        .map(|s| (s.instruction.0[0], s.potential_opcodes()))
        .for_each(|(opcode, candidates)| {
            candidates
                .iter()
                .for_each(|&candidate| {
                    stats
                        .get_mut(&opcode)
                        .and_then(|s| s.get_mut(candidate))
                        .and_then(|s| Some(*s += 1));
                });
        });

    stats
        .iter_mut()
        .for_each(|(_, hits)| {
            let max = *hits.values().max().unwrap();
            hits.extract_if(|_, count| *count != max).count();
        });

    let mut mapping: HashMap<&str, i32> = HashMap::new();

    while mapping.len() < 16 {
        let solved: HashMap<i32, &str> = stats
            .iter()
            .filter(|&(_, counts)| counts.len() == 1)
            .map(|(&opcode, counts)| (opcode, *counts.keys().last().unwrap()))
            .collect();

        solved
            .iter()
            .for_each(|(opcode, name)| {
                mapping.insert(*name, *opcode);
                stats.remove(opcode);
                stats
                    .values_mut()
                    .for_each(|counts| { counts.remove(name); });
            });
    }

    let instruction_set: HashMap<i32, fn(&mut Computer, i32, i32, i32)> = Computer::INSTRUCTION_SET
        .iter()
        .map(|(name, function)| (mapping[*name], *function))
        .collect();

    let mut computer = Computer::new();    
    program.
        iter()
        .map(|i| i.0)
        .for_each(|[op, a, b, c]| instruction_set[&op](&mut computer, a, b, c));
    
    *computer.register(0)
}

fn main() {
    let part = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let (samples, program) = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(samples))
    }
    else {
        println!("{}", part_two(samples, program))
    }
}

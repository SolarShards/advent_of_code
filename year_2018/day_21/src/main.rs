use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::{env, fs};

struct Registers([i64; 6]);
struct Instruction(fn(&mut Computer, i64, i64, i64), i64, i64, i64);
type Program = Vec<Instruction>;
struct Computer {
    registers: Registers,
    ip: usize,
    program: Program,
}

impl Computer {
    const INSTRUCTION_SET: [(&str, fn(&mut Computer, i64, i64, i64)); 16] = [
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
        ("eqrr", Computer::eqrr),
    ];

    fn new(ip: usize, program: Program) -> Computer {
        Computer {
            registers: Registers([0; 6]),
            ip,
            program,
        }
    }

    fn find_lower_bound(&mut self) -> i64 {
        let range = 0..self.program.len() as i64;
        let mut pc = 0;
        while range.contains(&pc) {
            if pc == (self.program.len() as i64 - 1) {
                return *self.register(4);
            }
            *self.register(self.ip as i64) = pc;
            let Instruction(f, a, b, c) = self.program[pc as usize];
            f(self, a, b, c);
            pc = *self.register(self.ip as i64);
            pc += 1;
        }

        panic!("Ran program without finding lower bound.")
    }

    fn find_upper_bound(&mut self) -> i64 {
        let range = 0..self.program.len() as i64;
        let mut pc = 0;
        let mut tested_values: HashSet<i64> = HashSet::new();
        let mut last = 0;
        while range.contains(&pc) {
            if pc == (self.program.len() as i64 - 1) {
                if tested_values.insert(*self.register(4)) {
                    last = *self.register(4);
                }
                else {
                    return last;
                }
            }
            *self.register(self.ip as i64) = pc;

            // Huge performance gain, deduced from analysing the input program
            if pc == 17 {
                *self.register(1) /= 256;
                *self.register(self.ip as i64) = 7;
            }
            else {
                let Instruction(f, a, b, c) = self.program[pc as usize];
                f(self, a, b, c);
            }

            pc = *self.register(self.ip as i64);
            pc += 1;
        }

        panic!("Ran program without finding upper bound.")
    }

    fn register(&mut self, reg: i64) -> &mut i64 {
        &mut self.registers.0[reg as usize]
    }

    fn addr(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = *self.register(a) + *self.register(b);
    }

    fn addi(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = *self.register(a) + b;
    }

    fn mulr(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = *self.register(a) * *self.register(b);
    }

    fn muli(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = *self.register(a) * b;
    }

    fn banr(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = *self.register(a) & *self.register(b);
    }

    fn bani(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = *self.register(a) & b;
    }

    fn borr(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = *self.register(a) | *self.register(b);
    }

    fn bori(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = *self.register(a) | b;
    }

    fn setr(&mut self, a: i64, _: i64, c: i64) {
        *self.register(c) = *self.register(a);
    }

    fn seti(&mut self, a: i64, _: i64, c: i64) {
        *self.register(c) = a;
    }

    fn gtir(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = (a > *self.register(b)) as i64;
    }

    fn gtri(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = (*self.register(a) > b) as i64;
    }

    fn gtrr(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = (*self.register(a) > *self.register(b)) as i64;
    }

    fn eqir(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = (a == *self.register(b)) as i64;
    }

    fn eqri(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = (*self.register(a) == b) as i64;
    }

    fn eqrr(&mut self, a: i64, b: i64, c: i64) {
        *self.register(c) = (*self.register(a) == *self.register(b)) as i64;
    }
}

fn read_input(filename: &str) -> Computer {
    let mut program: Program = Program::new();

    let file: String = fs::read_to_string(filename).unwrap();
    let ip = (file.as_bytes()[4] - b'0') as usize;

    let program_re: Regex = Regex::new(r"(\w+) (\d+) (\d+) (\d+)").unwrap();
    let instruction_set = HashMap::from(Computer::INSTRUCTION_SET);

    program_re.captures_iter(&file).for_each(|caps| {
        let tokens: [&str; 4] = caps.extract().1;
        let op = instruction_set[tokens[0]];
        let [a, b, c]: [i64; 3] = tokens[1..4]
            .iter()
            .map(|&x| x.parse::<i64>().unwrap())
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();

        program.push(Instruction(op, a, b, c));
    });

    Computer::new(ip, program)
}

fn part_one(mut computer: Computer) -> i64 {
    computer.find_lower_bound()
}

fn part_two(mut computer: Computer) -> i64 {
    computer.find_upper_bound()
}

fn main() {
    let part = env::args().nth(1).unwrap().parse::<i64>().unwrap();
    let computer = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(computer))
    } else {
        println!("{}", part_two(computer))
    }
}

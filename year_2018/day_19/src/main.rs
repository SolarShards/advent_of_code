use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::{env, fs};

struct Registers([i32; 6]);
struct Instruction(fn(&mut Computer, i32, i32, i32), i32, i32, i32);
type Program = Vec<Instruction>;
struct Computer {
    registers: Registers,
    ip: usize,
    program: Program,
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
        ("eqrr", Computer::eqrr),
    ];

    fn new(ip: usize, program: Program) -> Computer {
        Computer {
            registers: Registers([0; 6]),
            ip,
            program,
        }
    }

    fn run(&mut self) {
        let range = 0..self.program.len() as i32;
        let mut pc = 0;
        while range.contains(&pc) {
            *self.register(self.ip as i32) = pc;
            let Instruction(f, a, b, c) = self.program[pc as usize];
            f(self, a, b, c);
            pc = *self.register(self.ip as i32);
            pc += 1;
        }
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

fn read_input(filename: &str) -> Computer {
    let mut program: Program = Program::new();

    let file: String = fs::read_to_string(filename).unwrap();
    let ip = (file.as_bytes()[4] - b'0') as usize;

    let program_re: Regex = Regex::new(r"(\w+) (\d+) (\d+) (\d+)").unwrap();
    let instruction_set = HashMap::from(Computer::INSTRUCTION_SET);

    program_re.captures_iter(&file).for_each(|caps| {
        let tokens: [&str; 4] = caps.extract().1;
        let op = instruction_set[tokens[0]];
        let [a, b, c]: [i32; 3] = tokens[1..4]
            .iter()
            .map(|&x| x.parse::<i32>().unwrap())
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();

        program.push(Instruction(op, a, b, c));
    });

    Computer::new(ip, program)
}

fn part_one(mut computer: Computer) -> i32 {
    computer.run();
    *computer.register(0)
}

/// The analysis of the input program shows it does
/// the sum of all dividers of a number it computes
/// (A small number for part one, a big number for part 2).
/// Let's do it efficiently.
fn part_two(mut computer: Computer) -> i32 {
    *computer.register(0) = 1;
    computer.program.pop();
    computer.run();

    let number = *computer.register(2);
    let sqrt = (number as f32).sqrt() as i32;
    let mut dividers: HashSet<i32> = HashSet::new();

    (1..=sqrt).filter(|&i| number % i == 0).for_each(|i| {
        dividers.insert(i);
        dividers.insert(number / i);
    });

    dividers.iter().sum()
}

fn main() {
    let part = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let computer = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(computer))
    } else {
        println!("{}", part_two(computer))
    }
}

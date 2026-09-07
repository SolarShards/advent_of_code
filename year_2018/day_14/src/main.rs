use std::{env, fs};

struct Kitchen {
    elves: [usize; 2],
    board: Vec<u8>
}

impl Kitchen {
    fn new() -> Kitchen {
        Kitchen { elves: [0, 1], board: vec![3, 7] }
    }

    fn step(&mut self) {
        let sum: u8 = self.elves.iter().map(|&x| self.board[x]).sum();
        if sum > 9 {
            self.board.push(1);
        }
        self.board.push(sum % 10);
        self.elves.iter_mut().for_each(|x| *x = (*x + 1 + self.board[*x] as usize) % self.board.len());
    }
}

fn read_input(filename: &str) -> String {
    fs::read_to_string(filename).unwrap()
}

fn part_one(target: String) -> u64 {
    let target: usize = target.parse().unwrap();
    let mut kitchen = Kitchen::new();
    let mut answer: u64 = 0;

    while kitchen.board.len() < target + 10 {
        kitchen.step();
    }

    (target..(target+10)).for_each(|x| answer = answer * 10 + kitchen.board[x] as u64);

    answer
}

fn part_two(target: String) -> u64 {
    let target = Vec::from_iter(target.bytes().map(|x| x - b'0'));
    let mut kitchen = Kitchen::new();
    println!("{target:?}");

    loop {
        kitchen.step();
        if kitchen.board.ends_with(&target) {
            return (kitchen.board.len() - target.len()) as u64
        }
        else if kitchen.board[..(kitchen.board.len() - 1)].ends_with(&target) {
            return (kitchen.board.len() - target.len() - 1) as u64
        }
    }
}

fn main() {
    let part = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let input = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(input))
    }
    else {
        println!("{}", part_two(input))
    }
}

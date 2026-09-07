use std::{env, fs};
use std::collections::{HashSet, VecDeque};

struct Garden {
    state: HashSet<i32>,
    patterns: Vec<[bool; 5]>
}

impl Garden {

    fn step(&mut self) {
        let min = self.state.iter().min().unwrap() - 4;
        let max = self.state.iter().max().unwrap() + 4;
        let garden: Vec<bool> = (min..max).map(|x| self.state.contains(&x)).collect();
        let mut next_state: HashSet<i32> = HashSet::new();

        for i in 0..(garden.len() - 4) {
            let window = &garden[i..(i+5)];
            for pattern in self.patterns.iter() {
                if pattern == window {
                    next_state.insert(min + i as i32 + 2);
                    break;
                }
            }
        }

        self.state = next_state;
    }

    fn count(&self) -> i32 {
        self.state.iter().sum()
    }
}

fn read_input(filename: &str) -> Garden {

    let input= fs::read_to_string(filename).unwrap();
    let mut lines: VecDeque<&str>  = input.lines().collect();

    let init_state: HashSet<i32> = HashSet::from_iter(
        lines.pop_front().unwrap()
            .split_whitespace()
            .last().unwrap()
            .chars()
            .enumerate()
            .filter_map(|(i, s)| if s == '#' { Some(i as i32) } else { None })
    );

    lines.pop_front();

    let patterns: Vec<[bool; 5]> = Vec::from_iter(
        lines.iter()
        .filter(|line| line.chars().next_back().unwrap() == '#')
        .map(|&line| std::array::from_fn(|i| line[i..].chars().next().unwrap() == '#'))
    );

    Garden { state: init_state, patterns }
}

fn part_one(mut garden: Garden) -> i32 {
    const TARGET: i64 = 20;
    for _ in 0..TARGET {
        garden.step();
    }
    garden.count()
}

fn part_two(mut garden: Garden) -> i64 {
    const TARGET: i64 = 50_000_000_000;
    const CONVERGENCE_CRITERIA: u32 = 10;

    let mut generations: i64 = 0;
    let mut same_delta_count: u32 = 0;
    let mut count: i32 = 0;
    let mut delta: i32 = 0;

    while same_delta_count < CONVERGENCE_CRITERIA {

        garden.step();

        let c = garden.count();
        let d = c - count;

        if d == delta {
            same_delta_count += 1;
        }
        else {
            same_delta_count = 0;
        }

        generations += 1;
        count = c;
        delta = d;
    }

    count as i64 + (TARGET - generations) * delta as i64
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

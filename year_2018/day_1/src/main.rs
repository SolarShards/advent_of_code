use std::env;

use std::fs::File;
use std::io::{self, BufRead};

use std::collections::HashSet;

fn read_input(filename: &str) -> Vec<i32> {
    let file = File::open(filename)
        .expect("Failed to read the file {filename}");
    let reader = io::BufReader::new(file);

    reader.lines()
        .map(|line| line.unwrap().parse::<i32>().unwrap())
        .collect()
}

fn part_one(input: Vec<i32>) -> i32 {
    input.iter().sum()
}

fn part_two(input: Vec<i32>) -> i32 {
    let mut freqs = HashSet::new();
    let mut current = 0;
    freqs.insert(current);

    loop {
        for i in &input {
            current += i;
            if !freqs.insert(current) {
                return current
            }
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

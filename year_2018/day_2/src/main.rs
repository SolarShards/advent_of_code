use std::env;

use std::fs::File;
use std::io::{self, BufRead};

use std::collections::HashMap;
use std::iter::zip;

fn read_input(filename: &str) -> Vec<String> {
    let file = File::open(filename)
        .expect("Failed to read the file {filename}");
    let reader = io::BufReader::new(file);

    reader.lines().map(|line| line.unwrap()).collect()
}

fn part_one(input: Vec<String>) -> i32 {
    let mut pairs = 0;
    let mut triplets = 0;

    for id in input {
        let mut counter = HashMap::new();
        for letter in id.chars() {
            counter.entry(letter)
                .and_modify(|n| *n += 1)
                .or_insert(1);
        }
        if counter.values().any(|&x| x == 2) {
            pairs += 1;
        }
        if counter.values().any(|&x| x == 3) {
            triplets += 1;
        }
    }
    pairs * triplets
}

fn part_two(input: Vec<String>) -> String {
    let ids = input.iter().map(|x| x.chars().collect::<Vec<char>>()).collect::<Vec<Vec<char>>>();

    for (pos, id) in (&ids[..(ids.len()-1)]).iter().enumerate() {
        for other in &ids[(pos+1)..] {
            let mut distance = 0;

            for (c1, c2) in zip(id.iter(), other.iter()) {
                if c1 != c2 {
                    distance += 1
                }
            }

            if distance == 1 {
                let mut ret = String::new();
                for (c1, c2) in zip(id.iter(), other.iter()) {
                    if c1 == c2 {
                        ret.push(*c1);
                    }
                }
                return ret;
            }
        }
    }

    String::new()
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

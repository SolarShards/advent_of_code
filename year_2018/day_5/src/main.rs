use std::cmp::min;
use std::env;
use std::fs;

fn collapse_polymer(polymer: &mut Vec<u8>) {
    let mut last_len = polymer.len();
    loop {
        for i in (0..(last_len - 1)).rev() {
            if i == (polymer.len() - 1) {
                continue;
            }
            let c1 = &polymer[i];
            let c2 = &polymer[i+1];
            if (c1 != c2) && (c1.to_ascii_lowercase() == c2.to_ascii_lowercase()) {
                polymer.remove(i+1);
                polymer.remove(i);
            }
        }

        if polymer.len() == last_len {
            break;
        }
        else {
            last_len = polymer.len();
        }
    }
}

fn read_input(filename: &str) -> Vec<u8> {
    fs::read_to_string(filename).unwrap().bytes().collect::<Vec<u8>>()
}

fn part_one(mut input: Vec<u8>) -> u32 {
    collapse_polymer(&mut input);
    input.len() as u32
}

fn part_two(input: Vec<u8>) -> u32 {
    let mut shortest_len: u32 = u32::MAX;

    for c in b'a'..=b'z' {
        let unit = [c.to_ascii_lowercase(), c.to_ascii_uppercase()];
        let mut polymer = input.iter()
                               .copied()
                               .filter(|&x| !unit.contains(&x))
                               .collect::<Vec<_>>();
        collapse_polymer(&mut polymer);
        shortest_len = min(shortest_len, polymer.len() as u32);
    }

    shortest_len
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

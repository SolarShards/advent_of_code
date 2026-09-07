use std::collections::HashMap;
use std::{env, fs};

fn map_facility(regex: String) -> HashMap<(i32, i32), u32> {
    let unit_vectors =
        HashMap::from([('N', (0, -1)), ('E', (1, 0)), ('S', (0, 1)), ('W', (-1, 0))]);

    let mut rooms: HashMap<(i32, i32), u32> = HashMap::new();
    let mut branches: Vec<(i32, i32)> = Vec::new();
    let mut pos: (i32, i32) = (0, 0);
    let mut steps: u32 = 0;

    for direction in regex.chars() {
        match direction {
            'N' | 'E' | 'S' | 'W' => {
                let unit = unit_vectors[&direction];
                pos = (pos.0 + unit.0, pos.1 + unit.1);
                steps += 1;
                rooms
                    .entry(pos)
                    .and_modify(|v| *v = (*v).min(steps))
                    .or_insert(steps);
            }
            '(' => {
                branches.push(pos);
            }
            '|' => {
                pos = *branches.last().unwrap();
                steps = rooms[&pos];
            }
            ')' => {
                pos = branches.pop().unwrap();
                steps = rooms[&pos];
            }
            _ => (),
        }
    }

    rooms
}

fn read_input(filename: &str) -> String {
    fs::read_to_string(filename).unwrap()
}

fn part_one(regex: String) -> u32 {
    *map_facility(regex).values().max().unwrap()
}

fn part_two(regex: String) -> usize {
    map_facility(regex).values().filter(|&v| *v >= 1000).count()
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

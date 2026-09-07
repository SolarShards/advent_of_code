use std::{env, fs};
use std::cmp::{max, min};
use std::collections::{HashMap, HashSet};

use regex::Regex;
use itertools::Itertools;

struct Rectangle {
    x0: u16,
    y0: u16,
    x1: u16,
    y1: u16
}

impl Rectangle {

    fn new(x0: u16, y0: u16, x1: u16, y1: u16) -> Rectangle {
        assert!(x0 < x1, "Could not create the rectangle because x0 ({x0}) is greater than x1 ({x1})");
        assert!(y0 < y1, "Could not create the rectangle because y0 ({y0}) is greater than y1 ({y1})");
        Rectangle { x0, y0, x1, y1 }
    }

    fn intersect(&self, other: &Rectangle) -> Option<Rectangle> {
        let x0 = max(self.x0, other.x0);
        let y0 = max(self.y0, other.y0);
        let x1 = min(self.x1, other.x1);
        let y1 = min(self.y1, other.y1);

        if (x0 > x1) || (y0 > y1) {
            return None;
        }
        else {
            return Some(Rectangle { x0, y0, x1, y1 })
        }
    }

    fn to_square_inches(&self) -> HashSet<(u16, u16)> {
        let mut squares: HashSet<(u16, u16)> = HashSet::new();
        for x in self.x0..=self.x1 {
            for y in self.y0..=self.y1 {
                squares.insert((x, y));
            }
        }
        squares
    }
}

fn read_input(filename: &str) -> HashMap<u16, Rectangle> {
    let file = fs::read_to_string(filename).unwrap();

    let mut claims = HashMap::new();
    let re = Regex::new(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)").unwrap();

    re.captures_iter(&file).for_each(|caps| {
        let [id, x, y, w, h] = caps.extract().1.map(|x| x.parse::<u16>().unwrap());
        claims.insert(id, Rectangle::new(x, y, x+w-1, y+h-1));
    });

    claims
}

fn part_one(input: HashMap<u16, Rectangle>) -> u32 {
    let rects: Vec<Rectangle> = input.into_values().collect();
    let mut overlaps: HashSet<(u16, u16)> = HashSet::new();

    for [a, b] in rects.iter().array_combinations() {
        if let Some(r) = a.intersect(b) {
            overlaps.extend(r.to_square_inches());
        }
    }

    overlaps.len() as u32
}

fn part_two(input: HashMap<u16, Rectangle>) -> Result<u16, &'static str> {
    let mut overlapping: HashSet<u16> = HashSet::new();
    for [(id_a, a), (id_b, b)] in input.iter().array_combinations() {
        if let Some(_) = a.intersect(b) {
            overlapping.insert(*id_a);
            overlapping.insert(*id_b);
        }
    }
    
    for (idx, _) in input {
        if !overlapping.contains(&idx) {
            return Ok(idx);
        }
    }

    Err("Could not find the only claim that overlaps")
}

fn main() {
    let part = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let input = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(input))
    }
    else {
        println!("{}", part_two(input).unwrap())
    }
}

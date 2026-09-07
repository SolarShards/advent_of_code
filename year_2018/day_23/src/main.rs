use std::{env, fs};
use std::collections::BinaryHeap;

use regex::Regex;

struct Nanobot {
    x: i32,
    y: i32,
    z: i32,
    range: u32
}   

impl Nanobot {
    fn distance(&self, x: i32, y: i32, z: i32) -> u32 {
        self.x.abs_diff(x) + self.y.abs_diff(y) + self.z.abs_diff(z)
    }
}

#[derive(Clone)]
struct BoundingBox {
    min_x: i32,
    max_x: i32,
    min_y: i32,
    max_y: i32,
    min_z: i32,
    max_z: i32,
    upper_bound: u32
}

impl BoundingBox {
    fn new(min_x: i32, max_x: i32, min_y: i32, max_y: i32, min_z: i32, max_z: i32) -> BoundingBox {
        BoundingBox { min_x, max_x, min_y, max_y, min_z, max_z, upper_bound: 0 }
    }

    fn count_colliding_ranges(&mut self, nanobots: &Vec<Nanobot>) {
        self.upper_bound = nanobots
            .iter()
            .filter(|&n| {
                let x = n.x.clamp(self.min_x, self.max_x);
                let y = n.y.clamp(self.min_y, self.max_y);
                let z = n.z.clamp(self.min_z, self.max_z);
                n.distance(x, y, z) <= n.range
            })
            .count() as u32
    }

    fn is_point(&self) -> bool {
        (self.min_x.abs_diff(self.max_x) == 0) && (self.min_y.abs_diff(self.max_y) == 0) && (self.min_z.abs_diff(self.max_z) == 0)
    }

    fn octants(&self) -> Option<Vec<BoundingBox>> {
        if self.is_point() {
            return None
        }
        let mid_x = self.min_x.midpoint(self.max_x);
        let mid_y = self.min_y.midpoint(self.max_y);
        let mid_z = self.min_z.midpoint(self.max_z);

        let octs = [
            BoundingBox::new(self.min_x, mid_x, self.min_y, mid_y, self.min_z, mid_z),
            BoundingBox::new(mid_x + 1, self.max_x, self.min_y, mid_y, self.min_z, mid_z),
            BoundingBox::new(self.min_x, mid_x, mid_y + 1, self.max_y, self.min_z, mid_z),
            BoundingBox::new(self.min_x, mid_x, self.min_y, mid_y, mid_z + 1, self.max_z),
            BoundingBox::new(self.min_x, mid_x, mid_y + 1, self.max_y, mid_z + 1, self.max_z),
            BoundingBox::new(mid_x + 1, self.max_x, self.min_y, mid_y, mid_z + 1, self.max_z),
            BoundingBox::new(mid_x + 1, self.max_x, mid_y + 1, self.max_y, self.min_z, mid_z),
            BoundingBox::new(mid_x + 1, self.max_x, mid_y + 1, self.max_y, mid_z + 1, self.max_z)
        ]
            .iter()
            .filter(|o| o.max_x >= o.min_x && o.max_y >= o.min_y && o.max_z >= o.min_z)
            .cloned()
            .collect::<Vec<BoundingBox>>();

        Some(octs)
    }
}

impl PartialEq for BoundingBox {
    fn eq(&self, other: &Self) -> bool {
        self.upper_bound == other.upper_bound
    }
}

impl Eq for BoundingBox {}

impl PartialOrd for BoundingBox {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for BoundingBox {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.upper_bound.cmp(&other.upper_bound)
    }
}

fn read_input(filename: &str) -> Vec<Nanobot> {
    let file: String = fs::read_to_string(filename).unwrap();
    let mut nanobots: Vec<Nanobot> = Vec::new();

    Regex::new(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")
        .unwrap()
        .captures_iter(&file)
        .for_each(|caps| {
            let [x, y, z, r] = caps.extract().1.map(|x| x.parse::<i32>().unwrap());
            nanobots.push(Nanobot { x, y, z, range: r as u32 });
        });

    nanobots
}

fn part_one(nanobots: Vec<Nanobot>) -> u32 {
    let strongest = nanobots.iter().max_by_key(|&n| n.range).unwrap();
    nanobots
        .iter()
        .filter(|&n| strongest.distance(n.x, n.y, n.z) <= strongest.range)
        .count() as u32
}

fn part_two(nanobots: Vec<Nanobot>) -> u32 {
    let mut min_x = 0;
    let mut max_x = 0;
    let mut min_y = 0;
    let mut max_y = 0;
    let mut min_z = 0;
    let mut max_z = 0;

    nanobots.iter().for_each(|n| {
        min_x = min_x.min(n.x);
        max_x = max_x.max(n.x);
        min_y = min_y.min(n.y);
        max_y = max_y.max(n.y);
        min_z = min_z.min(n.z);
        max_z = max_z.max(n.z);
    });

    let mut octree = BinaryHeap::from([BoundingBox::new(min_x, max_x, min_y, max_y, min_z, max_z)]);
    let mut solutions: Vec<BoundingBox> = Vec::new();
    let mut max_bound: u32 = 0;

    while let Some(node) = octree.pop() {
        if node.is_point() {
            if max_bound == 0 {
                max_bound = node.upper_bound;
            }
            if node.upper_bound < max_bound {
                break;
            }
            solutions.push(node);
        }
        else if let Some(mut octants ) = node.octants() {
            octants.iter_mut().for_each(|octant| octant.count_colliding_ranges(&nanobots));
            let mut bh = BinaryHeap::from(octants);
            octree.append(&mut bh);
        }
    }

    solutions
        .iter()
        .map(|s| s.min_x.abs() + s.min_y.abs() + s.min_z.abs()).min().unwrap() as u32
}

fn main() {
    let part: i32 = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let input = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(input))
    }
    else {
        println!("{}", part_two(input))
    }
}
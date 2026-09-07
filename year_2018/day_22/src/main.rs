use std::{env, fs};
use regex::Regex;
use ndarray::Array2;
use pathfinding::prelude::astar;

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
enum Tool {
    Torch,
    ClimbingGear,
    None
}

#[derive(Clone, Copy)]
enum Region {
    Rocky = 0,
    Wet = 1,
    Narrow = 2
}

impl Region {
    fn tools(&self) -> [Tool; 2] {
        match *self {
            Region::Rocky => [Tool::ClimbingGear, Tool::Torch],
            Region::Wet => [Tool::ClimbingGear, Tool::None],
            Region::Narrow => [Tool::Torch, Tool::None]
        }
    }
}

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
struct Position(usize, usize, Tool);

impl Position {
    fn distance(&self, other: &Position) -> u32 {
        (self.0.abs_diff(other.0) + self.1.abs_diff(other.1)) as u32
    }

    fn successors(&self, map: &Array2<Region>) -> Vec<(Position, u32)> {
        let &Position(px, py, pt) = self;
        let mut next: Vec<(Position, u32)> = Vec::new();
        [(px, py.wrapping_sub(1)), (px+1, py), (px, py+1), (px.wrapping_sub(1) ,py)]
            .iter()
            .filter_map(|&(x, y)| {
                if let Some(r) = map.get((y, x)) {
                    Some((x, y, r))
                }
                else {
                    None
                }
            })
            .for_each(|(x, y, r)| {
                r.tools().iter().for_each(|&tool| {
                    next.push((Position(x, y, tool), if tool == pt { 1 } else { 8 }));
                });
            });

        next
  }
}

struct Cave {
    target: (usize, usize),
    map: Array2<Region>
}

impl Cave {
    fn new(depth: usize, target_x: usize, target_y: usize, rows_after_target: usize, cols_after_target: usize) -> Cave {
        let mut geo_map : Array2<u64> = Array2::zeros((target_y + 1 + rows_after_target, target_x + 1 + cols_after_target));
        let erosion_level = |geologic_index: u64| (geologic_index + depth as u64) % 20183;
        geo_map.row_mut(0).indexed_iter_mut().for_each(|(x, r)| *r = erosion_level(x as u64 * 16807));
        geo_map.column_mut(0).indexed_iter_mut().for_each(|(y, r)| *r = erosion_level(y as u64 * 48271));

        geo_map[[0, 0]] = erosion_level(0);
        
        (1..geo_map.dim().0).for_each(|y| {
            (1..geo_map.dim().1).for_each(|x| {
                if (x, y) == (target_x, target_y) {
                    geo_map[[y, x]] = erosion_level(0);
                }
                else {
                    geo_map[[y, x]] = erosion_level(geo_map[[y-1, x]] * geo_map[[y, x-1]]);
                }
            });
        });

        let erosion_map: Array2<Region> = geo_map.mapv(|erosion| {
            match erosion % 3 {
                0 => Region::Rocky,
                1 => Region::Wet,
                2 => Region::Narrow,
                _ => panic!("Invalid erosion level")
            }
        });

        Cave {target: (target_x, target_y), map: erosion_map }
    }

    fn risk_level(&self) -> u32 {
        self.map.map(|&x| x as u32).sum()
    }

    fn shortest_path_duration(&self) -> u32 {
        let target = Position(self.target.0, self.target.1, Tool::Torch);
        astar(
            &Position(0, 0, Tool::Torch),
            |p| p.successors(&self.map),
            |p| p.distance(&target),
            |p| *p == target
        ).unwrap().1
    }
}

fn read_input(filename: &str) -> (usize, usize, usize) {
    let scan = fs::read_to_string(filename).unwrap();
    let matches = Regex::new(r"\d+")
        .unwrap()
        .find_iter(&scan)
        .map(|m| m.as_str().parse::<usize>().unwrap())
        .collect::<Vec<usize>>();
    (matches[0], matches[1], matches[2])
}

fn part_one(depth: usize, x: usize, y: usize) -> u32 {
    Cave::new(depth, x, y, 0, 0).risk_level()
}

fn part_two(depth: usize, x: usize, y: usize) -> u32 {
    Cave::new(depth, x, y, 50, 50).shortest_path_duration()
}

fn main() {
    let part = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let (depth, x, y) = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(depth, x, y))
    } else {
        println!("{}", part_two(depth, x, y))
    }
}

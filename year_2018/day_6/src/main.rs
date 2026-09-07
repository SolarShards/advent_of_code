use std::env;
use std::fs;
use std::collections::HashMap;

use regex::Regex;
use ndarray::Array2;

struct Point { x: u32, y: u32 }

impl Point {
    fn manhattan_distance(&self, x: u32, y: u32) -> u32 {
        x.abs_diff(self.x) + y.abs_diff(self.y)
    }
}

fn read_input(filename: &str) -> HashMap<u8, Point> {
    let file = fs::read_to_string(filename).unwrap();
    let re = Regex::new(r"(\d+), (\d+)").unwrap();
    let mut points = HashMap::new();
    let mut id: u8 = b'1';

    re.captures_iter(&file).for_each(|caps| {
        let [x, y] = caps.extract().1.map(|x| x.parse::<u32>().unwrap());
        points.insert(id, Point{x, y});
        id += 1;
    });

    points
}

fn part_one(input: HashMap<u8, Point>) -> u32 {

    // define the area containing all points
    let min_x = input.values().min_by_key(|&p| p.x).unwrap().x as u32;
    let max_x = input.values().max_by_key(|&p| p.x).unwrap().x as u32;
    let min_y = input.values().min_by_key(|&p| p.y).unwrap().y as u32;
    let max_y = input.values().max_by_key(|&p| p.y).unwrap().y as u32;

    // choose the number of rows and cols of the matrix
    // (no real thought here, adding a padding of the mins worked well for my input)
    let rows = (max_y + min_y) as usize;
    let cols = (max_x + min_x) as usize;

    // Init the matrix
    let mut map = Array2::<u8>::from_elem((rows, cols), b' ');

    // write the ID of the closest point to each coordinate in the matrix
    for y in 0..(cols as u32) {
        for x in 0..(rows as u32) {
            let mut distances = input.iter()
                .map(|(id, p)| (id, p.manhattan_distance(x, y)))
                .collect::<Vec<_>>();
            distances.sort_by_key(|(_id, distance)| *distance);

            if distances[0].1 != distances[1].1 {
                map[[x as usize, y as usize]] = *distances[0].0;
            }
        }
    }

    // create an iterator that filters out points with infinite areas
    let finite_area_points = input.iter().filter(
        |&(id, _p)| {

            for bound in [map.row(0), map.row(rows-1), map.column(0), map.column(cols-1)] {
                if bound.iter().any(|i| *i == *id) {
                    return false;
                }
            }

            true
        }
    );

    // count the occurences of each ID in the matrix
    let mut areas: HashMap<u8, u32> = HashMap::new();
    for (id, _) in finite_area_points {
        areas.insert(*id, 0);
    }

    for id in map.iter() {
        if let Some(count) = areas.get_mut(&id) {
            *count += 1;
        }
    }

    // print in file -- it displays well when zoomed out in VSCode or KWrite
    /* 
    let mut file = File::create("display.txt").unwrap();
    for row in map.rows() {
        let _ = file.write(row.as_slice().unwrap());
        let _ = file.write(b"\n");
    }
    */

    areas.values().max().copied().unwrap()
}

fn part_two(input: HashMap<u8, Point>) -> u32 {

    const MAX_DISTANCE: u32 = 10000;

    // define the area containing all points
    let min_x = input.values().min_by_key(|&p| p.x).unwrap().x as u32;
    let max_x = input.values().max_by_key(|&p| p.x).unwrap().x as u32;
    let min_y = input.values().min_by_key(|&p| p.y).unwrap().y as u32;
    let max_y = input.values().max_by_key(|&p| p.y).unwrap().y as u32;

    // choose the number of rows and cols of the matrix
    // (no real thought here, adding a padding of the mins worked well for my input)
    let rows = (max_y + min_y) as usize;
    let cols = (max_x + min_x) as usize;

    let mut area = 0;

    for y in 0..(cols as u32) {
        for x in 0..(rows as u32) {
            let cumulated_distances: u32 = input.iter()
                .map(|(_id, p)| p.manhattan_distance(x, y))
                .sum();
            if cumulated_distances < MAX_DISTANCE {
                area += 1;
            }
        }
    }

    area
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

use std::fs;
use std::collections::HashSet;

use regex::Regex;

fn read_input(filename: &str) -> HashSet<(i32, i32, i32, i32)> {
    let input = fs::read_to_string(filename).unwrap();
    Regex::new(r"(-?\d+),(-?\d+),(-?\d+),(-?\d+)")
        .unwrap()
        .captures_iter(&input)
        .map(|caps| {
            let [x, y, z, t] = caps.extract().1.map(|x| x.parse::<i32>().unwrap());
            (x, y, z, t)
        })
        .collect()
}

fn part_one(mut points: HashSet<(i32, i32, i32, i32)>) -> i32 {
    let mut count = 0i32;
    while let Some(p) = points.iter().next().cloned() {
        points.remove(&p);
        let mut constellation = Vec::from([p]);

        while let Some((x1, y1, z1, t1)) = constellation.pop() {
            let mut linked = points
                .extract_if(|&(x2, y2, z2, t2)| {
                    x1.abs_diff(x2) + y1.abs_diff(y2) + z1.abs_diff(z2) + t1.abs_diff(t2) <= 3
                }).collect::<Vec<_>>();
            constellation.append(&mut linked);
        }

        count += 1;
    }

    count
}

fn main() {
    let points = read_input("input.txt");
    println!("{}", part_one(points));
}
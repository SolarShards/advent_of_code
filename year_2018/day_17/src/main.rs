use std::{env, fs};
use std::collections::HashSet;
use std::ops::RangeInclusive;

use regex::Regex;

struct Scan {
    clay_areas: HashSet<(i32, i32)>,
    min_x: i32,
    max_x: i32,
    min_y: i32,
    max_y: i32
}

impl Scan {
    fn in_bounds(&self, (x, y): &(i32, i32)) -> bool {
        (self.min_x..=self.max_x).contains(x) && (self.min_y..=self.max_y).contains(y)
    }

    fn simulate_water_flow(&self) -> (usize, usize) {
        let mut open_list: Vec<(i32, i32)> = vec![(500, self.min_y)];
        let mut flowing_water: HashSet<(i32, i32)> = HashSet::new();
        let mut still_water: HashSet<(i32, i32)> = HashSet::new();

        while let Some((x, mut y)) = open_list.pop() {

            // Over scan bound or flowing water -> flowing water
            if !self.in_bounds(&(x, y+1)) || flowing_water.contains(&(x, y+1)) {
                flowing_water.insert((x, y));
            }

            // Over clay or still water -> manage horizontal flow or reservoir filling
            else if self.clay_areas.contains(&(x, y+1)) || still_water.contains(&(x, y+1)) {
                let mut row: Vec<(i32, i32)> = vec![(x, y)];
                let mut dropdowns: Vec<(i32, i32)> = Vec::new();

                for step in [-1, 1] {
                    let mut dx: i32 = x + step;
                    while !self.clay_areas.contains(&(dx, y)) {
                        if !self.clay_areas.contains(&(dx, y+1)) && !still_water.contains(&(dx, y+1)) {
                            dropdowns.push((dx, y));
                            break;
                        }
                        else {
                            row.push((dx, y));
                            dx += step;
                        }
                    }
                }

                if dropdowns.is_empty() {
                    still_water.extend(row);
                    still_water.iter().for_each(|p| { flowing_water.remove(p); });
                }
                else {
                    flowing_water.extend(row);
                    open_list.extend(dropdowns);
                }
            }

            // Over sand -> flow down and fill open list until anything is met
            else {
                while self.in_bounds(&(x, y))
                    && !self.clay_areas.contains(&(x, y))
                    && !flowing_water.contains(&(x, y))
                    && !still_water.contains(&(x, y))
                {
                    open_list.push((x, y));
                    y += 1;
                }
            }
        }

        /* Print code (prints line in the puzzle explanation)

        let map: Vec<Vec<u8>> = (self.min_y..= self.max_y)
            .map(|y| {
                (self.min_x..= self.max_x)
                    .map(|x| {
                        if self.clay_areas.contains(&(x, y)){
                            b'#'
                        } 
                        else if flowing_water.contains(&(x, y)) {
                            b'|'
                        }
                        else if still_water.contains(&(x, y)){
                            b'~'
                        }
                        else {
                            b' '
                        }
                    })
                    .collect()
            })
            .collect();

        let mut file = fs::File::create("display.txt").unwrap();
        for line in &map {
            let _ = std::io::Write::write(&mut file, &line);
            let _ = std::io::Write::write(&mut file, b"\n");
        }
         */
            
        (flowing_water.len(), still_water.len())
    }
}

fn read_input(filename: &str) -> Scan {
    let mut rows: Vec<(RangeInclusive<i32>, i32)> = Vec::new();
    let mut cols: Vec<(i32, RangeInclusive<i32>)> = Vec::new();
    let mut min_x: i32 = i32::MAX;
    let mut max_x: i32 = i32::MIN;
    let mut min_y: i32 = i32::MAX;
    let mut max_y: i32 = i32::MIN;

    let file: String = fs::read_to_string(filename).unwrap();

    Regex::new(r"y=(\d+), x=(\d+)..(\d+)")
        .unwrap()
        .captures_iter(&file)
        .for_each(|caps| {
            let [y, low_x, high_x] = caps
                .extract().1
                .map(|x| x.parse::<i32>().unwrap());
            rows.push((low_x..=high_x, y));
            min_x = min_x.min(low_x);
            max_x = max_x.max(high_x);
            min_y = min_y.min(y);
            max_y = max_y.max(y);
        });

    Regex::new(r"x=(\d+), y=(\d+)..(\d+)")
        .unwrap()
        .captures_iter(&file)
        .for_each(|caps| {
            let [x, low_y, high_y] = caps
                .extract().1
                .map(|x| x.parse::<i32>().unwrap());
            cols.push((x, low_y..=high_y));
            min_x = min_x.min(x);
            max_x = max_x.max(x);
            min_y = min_y.min(low_y);
            max_y = max_y.max(high_y);
        });

    min_x -= 1;
    max_x += 1;

    let mut clay_areas = rows
        .iter()
        .map(|(x_range, y)| {
            x_range.clone().map(|x| (x, *y)).collect::<Vec<(i32, i32)>>()
        })
        .collect::<Vec<Vec<(i32, i32)>>>()
        .concat();

    let mut other_clay_areas = cols
        .iter()
        .map(|(x, y_range)| {
            y_range.clone().map(|y| (*x, y)).collect::<Vec<(i32, i32)>>()
        })
        .collect::<Vec<Vec<(i32, i32)>>>()
        .concat();

    clay_areas.append(&mut other_clay_areas);
    let clay_areas: HashSet<(i32, i32)> = clay_areas.into_iter().collect::<HashSet<(i32, i32)>>();
    
    Scan { clay_areas, min_x, max_x, min_y, max_y }
}

fn part_one(scan: Scan) -> usize {
    let (flowing, still) = scan.simulate_water_flow();
    flowing + still
}

fn part_two(scan: Scan) -> usize {
    scan.simulate_water_flow().1
}

fn main() {
    let part = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let map = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(map))
    }
    else {
        println!("{}", part_two(map))
    }
}

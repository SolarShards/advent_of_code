use std::env;
use std::fs;

use regex::Regex;
use tesseract::Tesseract;

struct Point {
    x: i32,
    y: i32,
    vx: i32,
    vy: i32
}

impl Point {
    fn step(&mut self) {
        self.x += self.vx;
        self.y += self.vy;
    }

    fn step_back(&mut self) {
        self.x -= self.vx;
        self.y -= self.vy;
    }
}

enum Output {
    Message(String),
    Steps(u32)
}

fn read_message(points: &mut Vec<Point>, part: u32) -> Output {
    let mut steps: u32 = 0;
    let mut last_height = usize::MAX;
    let mut height = usize::MAX - 1;
    let mut min_y= 0;
    let mut max_y;
    
    while height < last_height {

        last_height = height;

        for p in points.iter_mut() {
            p.step();
        }

        min_y = points.iter().map(|p| p.y).min().unwrap();
        max_y = points.iter().map(|p| p.y).max().unwrap();
        height = (max_y.abs_diff(min_y) + 1) as usize;

        steps += 1
    }

    if part == 2 {
        return Output::Steps(steps-1);
    }

    for p in points.iter_mut() {
        p.step_back();
    }

    let min_x = points.iter().map(|p| p.x).min().unwrap();
    let max_x = points.iter().map(|p| p.x).max().unwrap();
    let width = (max_x.abs_diff(min_x) + 1) as usize;

    let mut display: Vec<u8> = vec![255; width * height];
    for p in points.iter() {
        let idx = (p.y - min_y) as usize * width + (p.x - min_x) as usize;
        display[idx] = 0;
    }

    let message = Tesseract::new(None, Some("eng"))
        .unwrap()
        .set_frame(&display, width as i32, height as i32, 1, width as i32)
        .unwrap()
        .get_text()
        .unwrap()
        .split_whitespace()
        .collect();

    /* Print in file to compare with OCR

    let mut display = vec![b' '; width * height];
    for p in input.iter() {
        let idx = (p.y - min_y) as usize * width + (p.x - min_x) as usize;
        display[idx] = b'X';
    }

    let mut file = File::create("display.txt").unwrap();

    for y in 0..height {
        let _ = file.write(&display[(y * width)..((y+1) * width)]);
        let _ = file.write(b"\n");
    }
    */

    Output::Message(message)
}

fn read_input(filename: &str) -> Vec<Point> {
    let file: String = fs::read_to_string(filename).unwrap();
    let re: Regex = Regex::new(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>").unwrap();
    let mut points: Vec<Point> = Vec::new();

    re.captures_iter(&file).for_each(|caps| {
        let [x, y, vx, vy] = caps.extract().1.map(|x| x.parse::<i32>().unwrap());
        points.push(Point { x, y, vx, vy });
    });

    points
}

fn part_one(mut input: Vec<Point>) -> String {
    if let Output::Message(m) = read_message(&mut input, 1) {
        m
    }
    else {
        panic!()
    }
}

fn part_two(mut input: Vec<Point>) -> u32 {
    if let Output::Steps(s) = read_message(&mut input, 2) {
        s
    }
    else {
        panic!()
    }
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
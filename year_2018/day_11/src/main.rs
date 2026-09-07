use std::env;
use std::fs;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;
use ndarray::Array2;

struct Battery {
    grid: Array2<i32>
}

impl Battery {
    fn new(serial_number: i32) -> Battery {
        Battery {
            grid: Array2::<i32>::from_shape_fn((300, 300), |(x, y)| {
                let rack_id = x as i32 + 1 + 10;
                (rack_id * (y as i32 + 1) + serial_number) * rack_id / 100 % 10 - 5
            })
        }
    }

    fn most_charged_area(&self, size: usize) -> (u32, u32, i32){
        let (idx, block) = self.grid.windows((size, size))
        .into_iter()
        .enumerate()
        .max_by_key(|&(_, block)| block.sum())
        .unwrap();
        let windowed_size = 300 - size + 1;
        ((idx / windowed_size + 1) as u32, (idx % windowed_size + 1) as u32, block.sum() as i32)
    }
}

fn read_input(filename: &str) -> i32 {
    fs::read_to_string(filename)
        .unwrap()
        .parse::<i32>()
        .unwrap()
        
}

fn part_one(input: i32) -> (u32, u32) {
    let (x, y, _) = Battery::new(input).most_charged_area(3);
    (x, y)
}

fn part_two(input: i32) -> (u32, u32, u32) {
    let battery = Arc::new(Battery::new(input));
    let maximums = Arc::new(Mutex::new(Vec::<(usize, (u32, u32, i32))>::new()));
    let mut threadpool = Vec::new();

    for size in 2..=300 {
        let battery = Arc::clone(&battery);
        let maximums = Arc::clone(&maximums);
        let t = thread::spawn(move || {
            let result = (size, battery.most_charged_area(size));
            maximums.lock().unwrap().push(result);
        });
        threadpool.push(t);
    }

    for t in threadpool {
        t.join().unwrap();
    }

    let (size, (x, y, _)) = *maximums
        .lock()
        .unwrap()
        .iter()
        .max_by_key(|&(_, (_, _, p))| p)
        .unwrap();

    (x, y, size as u32)
}

fn main() {
    let part: i32 = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let input = read_input("input.txt");
    if part == 1 {
        let (x, y) = part_one(input);
        println!("{x},{y}")
    }
    else {
        let (x, y, s) = part_two(input);
        println!("{x},{y},{s}")
    }
}

use std::{env, fs};
use std::collections::HashMap;
use ndarray::Array2;

#[derive(Clone, PartialEq, Debug)]
enum Acre {
    OPEN,
    TREES,
    LUMBERYARD
}

struct Area(Array2<Acre>);

impl Area {

    const OFFSETS: [(isize, isize); 8] = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ];

    fn change(&mut self) {
        let shape = self.0.dim();
        let new_state = Array2::from_shape_fn(shape, |(row, col)| {
            let mut trees = 0;
            let mut lumberyards = 0;

            Area::OFFSETS.iter().for_each(|&(r, c)| {
                let r = (row as isize + r) as usize;
                let c = (col as isize + c) as usize;
                match self.0.get((r, c)) {
                    Some(Acre::TREES) => trees += 1,
                    Some(Acre::LUMBERYARD) => lumberyards += 1,
                    _ => ()
                }
            });

            match self.0.get((row, col)) {
                Some(Acre::OPEN) => if trees >= 3 {Acre::TREES} else {Acre::OPEN},
                Some(Acre::TREES) => if lumberyards >= 3 {Acre::LUMBERYARD} else {Acre::TREES},
                Some(Acre::LUMBERYARD) => if (trees > 0) && (lumberyards > 0) {Acre::LUMBERYARD} else {Acre::OPEN},
                _ => panic!()
            }
        });
        self.0 = new_state;
    }

    fn ressource_value(&self) -> usize {
        self.0.iter().filter(|&x| *x == Acre::TREES).count() * self.0.iter().filter(|&x| *x == Acre::LUMBERYARD).count()
    }
}

fn read_input(filename: &str) -> Area {

    let input = fs::read_to_string(filename).unwrap();
    let rows = input.lines().count();
    let cols = input.lines().next().unwrap().len();

    let map: Vec<Acre> = input
        .replace('\n', "")
        .bytes()
        .map(|c| {
            match c {
                b'|' => Acre::TREES,
                b'#' => Acre::LUMBERYARD,
                _ => Acre::OPEN
            }
        })
        .collect();

    Area(Array2::from_shape_vec((rows, cols), map).unwrap())
}

fn part_one(mut area: Area) -> usize {
    for _ in 0..10 {
        area.change();
    }

    area.ressource_value()
}

fn part_two(mut area: Area) -> usize {
    const CRITERIA: u32 = 5;

    let mut counter: HashMap<usize, u32> = HashMap::from([(area.ressource_value(), 1)]);
    let mut count: u32 = 0;
    let mut elapsed: usize = 0;

    while count < CRITERIA  {
        area.change();
        elapsed += 1;
        counter
            .entry(area.ressource_value())
            .and_modify(|e| {
                *e += 1;
                count = count.max(*e);
            })
            .or_insert(1);
    }

    let mut cycle = vec![area.ressource_value()];
    area.change();
    let mut value = area.ressource_value();

    while value != cycle[0] {
        cycle.push(value);
        area.change();
        value = area.ressource_value();
    }

    cycle[(1_000_000_000 - elapsed) % cycle.len()]
}

fn main() {
    let part = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let area = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(area))
    }
    else {
        println!("{}", part_two(area))
    }
}

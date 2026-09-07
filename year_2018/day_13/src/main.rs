use std::{env, fs};
use std::collections::BTreeMap;
use ndarray::Array2;

#[derive(Copy, Clone, Debug)]
enum Orientation {
    NORTH,
    EAST,
    SOUTH,
    WEST
}

#[derive(Debug)]
enum Direction {
    LEFT,
    STRAIGHT,
    RIGHT
}

#[derive(Debug)]
struct Cart {
    orientation: Orientation,
    next_turn: Direction
}

impl Cart {

    fn new(orientation: Orientation) -> Cart {
        Cart { orientation, next_turn: Direction::LEFT }
    }

    fn select_direction(&mut self, track: u8) {
        
        self.orientation = match track {
            b'/' => {
                match self.orientation {
                    Orientation::NORTH => Orientation::EAST,
                    Orientation::EAST => Orientation::NORTH,
                    Orientation::SOUTH => Orientation::WEST,
                    Orientation::WEST => Orientation::SOUTH
                }
            },
            b'\\' => {
                match self.orientation {
                    Orientation::NORTH => Orientation::WEST,
                    Orientation::EAST => Orientation::SOUTH,
                    Orientation::SOUTH => Orientation::EAST,
                    Orientation::WEST => Orientation::NORTH
                }
            },
            b'+' => {
                match self.next_turn {
                    Direction::LEFT => {
                        self.next_turn = Direction::STRAIGHT;
                        match self.orientation {
                            Orientation::NORTH => Orientation::WEST,
                            Orientation::EAST => Orientation::NORTH,
                            Orientation::SOUTH => Orientation::EAST,
                            Orientation::WEST => Orientation::SOUTH
                        }
                    },
                    Direction::STRAIGHT => {
                        self.next_turn = Direction::RIGHT;
                        self.orientation
                    },
                    Direction::RIGHT => {
                        self.next_turn = Direction::LEFT;
                        match self.orientation {
                            Orientation::NORTH => Orientation::EAST,
                            Orientation::EAST => Orientation::SOUTH,
                            Orientation::SOUTH => Orientation::WEST,
                            Orientation::WEST => Orientation::NORTH
                        }
                    },
                }
            },
            b' ' => panic!("Derailed {self:?}"),
            _ => self.orientation
        };
    }
}

struct TrackSystem {
    carts: BTreeMap<(usize, usize), Cart>,
    tracks: Array2<u8>
}

impl TrackSystem {
    fn tick(&mut self) -> Option<Vec<(usize, usize)>> {
        let mut new_positions = BTreeMap::new();
        let mut collisions = Vec::new();

        while let Some(((y, x), mut c)) = self.carts.pop_first() {
            c.select_direction(self.tracks[[y, x]]);
            let new_pos = match c.orientation {
                    Orientation::NORTH => (y-1, x),
                    Orientation::EAST => (y, x+1),
                    Orientation::SOUTH => (y+1, x),
                    Orientation::WEST => (y, x-1)
                };
            
            if self.carts.contains_key(&new_pos) {
                self.carts.remove(&new_pos);
                collisions.push(new_pos);
            }
            else if new_positions.contains_key(&new_pos) {
                new_positions.remove(&new_pos);
                collisions.push(new_pos);
            }
            else {
                new_positions.insert(new_pos, c);
            }
        };

        self.carts = new_positions;

        if collisions.is_empty() { None } else { Some(collisions) }
    }
}

fn read_input(filename: &str) -> TrackSystem {
    let map = fs::read_to_string(filename).unwrap();
    let rows = map.lines().count();
    let cols = map.lines().next().unwrap().len();
    let flattened: Vec<u8> = map.lines()
        .flat_map(|line| line.as_bytes().iter().copied())
        .collect();
    let mut tracks = Array2::from_shape_vec((rows, cols), flattened).unwrap();

    let mut carts = BTreeMap::new();

    tracks.indexed_iter_mut()
        .for_each(|((r, c), v)| {
            match v {
                b'^' => {
                    carts.insert((r,c), Cart::new(Orientation::NORTH));
                    *v = b'|';
                },
                b'>' => {
                    carts.insert((r,c), Cart::new(Orientation::EAST));
                    *v = b'-';
                },
                b'v' => {
                    carts.insert((r,c), Cart::new(Orientation::SOUTH));
                    *v = b'|';
                },
                b'<' => {
                    carts.insert((r,c), Cart::new(Orientation::WEST));
                    *v = b'-';
                },
                _ => ()
            }
        });

    TrackSystem { carts, tracks }
}

fn part_one(mut tracks: TrackSystem) -> String {
    let mut collisions = None;

    while collisions == None {
        collisions = tracks.tick();
    }

    let c = collisions.unwrap()[0];
    format!("{},{}", c.1, c.0)
}

fn part_two(mut tracks: TrackSystem) -> String {
    while tracks.carts.len() > 1 {
        tracks.tick();
    }

    let c = tracks.carts.first_key_value().unwrap().0;
    format!("{},{}", c.1, c.0)
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

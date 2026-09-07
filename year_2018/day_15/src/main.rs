use std::{env, fs};
use std::collections::{HashMap, HashSet};

use ndarray::Array2;
use pathfinding::prelude::bfs;

#[derive(Clone)]
enum Tile {
    Floor,
    Wall,
    Unit
}

#[derive(PartialEq, Clone)]
enum Race {
    Elf,
    Goblin
}

#[derive(Clone)]
struct Unit {
    x: usize,
    y: usize,
    hp: i16,
    ad: i16,
    race: Race
}

impl Unit {
    fn new(x: usize, y: usize, race: Race) -> Unit {
        Unit { x, y, hp: 200, ad: 3, race }
    }
    
}

#[derive(Clone)]
struct Arena {
    map: Array2<Tile>,
    units: HashMap<u32, Unit>
}

impl Arena {

    fn define_turn_order(&self) -> Vec<u32> {
        let mut indexed = self.units.iter().map(|(&k, v)| (k, v)).collect::<Vec<(u32, &Unit)>>();
        indexed.sort_unstable_by_key(|(_, unit)| (unit.y, unit.x));
        indexed.iter().map(|&(idx, _)| idx).collect()
    }

    fn enemies(&self, id: u32) -> Option<Vec<u32>> {
        let Some(unit) = self.units.get(&id) else { return None; };
        let enemies = self.units
            .iter()
            .filter_map(|(&id, other)| {
                if unit.race != other.race {
                    Some(id)
                }
                else {
                    None
                }
            })
            .collect::<Vec<u32>>();
        if enemies.is_empty() { None } else { Some(enemies) }
    }

    fn try_attack(&mut self, id: u32) -> bool {
        let Some(unit) = self.units.get(&id) else { return false; };
        let target = [(unit.x, unit.y-1), (unit.x+1, unit.y), (unit.x, unit.y+1), (unit.x-1, unit.y)]
            .iter()
            .filter_map(|&(x, y)| {
                if let Tile::Unit = self.map[[y, x]] {
                    self.units.iter().find(|&(&_, u)| (u.x == x) && (u.y == y) && (u.race != unit.race))
                }
                else{
                    None
                }
            })
            .min_by_key(|(_, u)| (u.hp, u.y, u.x))
            .and_then(|(&id, _)| Some(id));

        if let Some(id) = target {
            let damage = unit.ad;
            let u = self.units.get_mut(&id).unwrap();
            u.hp -= damage;
            if u.hp <= 0 {
                self.map[[u.y, u.x]] = Tile::Floor;
                self.units.remove(&id);
            }
            return true;
        }
        else {
            return false
        };
    }

    fn adjacent_floors(&self, id: u32) -> Option<Vec<(usize, usize)>> {
        let Some(unit) = self.units.get(&id) else { return None; };
        let floors = [(unit.x, unit.y-1), (unit.x+1, unit.y), (unit.x, unit.y+1), (unit.x-1, unit.y)]
            .iter()
            .filter_map(|&(x, y)| {
                if let Tile::Floor = self.map[[y, x]] {
                    Some((x,y))
                }
                else{
                    None
                }
            })
            .collect::<Vec<(usize, usize)>>();
        if floors.is_empty() { None } else { Some(floors) }
    }

   fn select_target_and_move(&mut self, id: u32, targets: &Vec<u32>) {
        let floors = targets
            .iter()
            .filter_map(|&i| self.adjacent_floors(i))
            .collect::<Vec<Vec<(usize, usize)>>>()
            .concat()
            .into_iter()
            .collect::<HashSet<(usize, usize)>>();

        let Some(unit) = self.units.get_mut(&id) else { return };

        let Some((_, path)) = floors
            .iter()
            .filter_map(|&(target_x, target_y)| {
                bfs(
                    &(unit.x, unit.y),
                    |&(x, y)| {
                        [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
                            .iter()
                            .filter_map(|&(x, y)| {
                                if let Some(Tile::Floor) = self.map.get((y, x)) {
                                    Some((x, y))
                                }
                                else {
                                    None
                                }
                            })
                            .collect::<Vec<_>>()
                    },
                    |&(x, y)| (x, y) == (target_x, target_y)
                )
                .map(|path| ((target_y, target_x), path))
            })
            .min_by_key(|((target_y, target_x), path)| {
                (path.len(), *target_y, *target_x, path[1].1, path[1].0)
            })
            else {
                return
            };

        let (x, y) = path[1];
        self.map[[unit.y, unit.x]] = Tile::Floor;
        unit.x = x;
        unit.y = y;
        self.map[[unit.y, unit.x]] = Tile::Unit;

   }

    fn run_fight(&mut self) -> u32 {
        let mut turns: u32 = 0;
        
        'mainloop: loop {
            for id in self.define_turn_order() {
                if !self.units.contains_key(&id) {
                    continue;
                }

                let Some(enemies) = self.enemies(id)
                else {
                    break 'mainloop 
                };

                if self.try_attack(id) {
                    continue;
                }

                self.select_target_and_move(id, &enemies);

                self.try_attack(id);
                
            }
            turns += 1;
        }

        turns * self.units.iter().map(|(_, u)| u.hp as u32).sum::<u32>()
    }

    fn count_elves(&self) -> usize {
        self.units
            .iter()
            .filter(|(_, u)| u.race == Race::Elf)
            .count()
    }
}

fn read_input(filename: &str) -> Arena {
    let input = fs::read_to_string(filename).unwrap();
    let rows = input.lines().count();
    let cols = input.lines().next().unwrap().len();
    let mut units: HashMap<u32, Unit> = HashMap::new();
    let mut flattened: Vec<Tile> = Vec::new();
    let mut id: u32 = 0;
    for (row, line) in input.lines().enumerate() {
        for (col, &tile) in line.as_bytes().iter().enumerate() {
            match tile {
                b'E' => {
                    units.insert(id, Unit::new(col, row, Race::Elf));
                    flattened.push(Tile::Unit);
                    id += 1;
                },
                b'G' => {
                    units.insert(id, Unit::new(col, row, Race::Goblin));
                    flattened.push(Tile::Unit);
                    id += 1;
                },
                b'.' => {
                    flattened.push(Tile::Floor);
                },
                _ => {
                    flattened.push(Tile::Wall);
                },
            }
        }
    }

    let map = Array2::from_shape_vec((rows, cols), flattened).unwrap();
    Arena { map, units }
}

fn part_one(mut arena: Arena) -> u32 {
    arena.run_fight()
}

fn part_two(arena: Arena) -> u32 {
    let mut bonus_ad: i16 = 1;
    let elf_count = arena.count_elves();
    let mut outcome;
    loop {
        let mut arena = arena.clone();
        arena.units
            .iter_mut()
            .filter(|(_, u)| u.race == Race::Elf)
            .for_each(|(_, u)| u.ad += bonus_ad);
        outcome = arena.run_fight();
        if arena.count_elves() == elf_count {
            break;
        }
        bonus_ad += 1;
    }
    outcome
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

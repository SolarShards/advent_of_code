use std::env;
use std::fs;
use std::rc::{Rc, Weak};
use std::cell::RefCell;

use itertools::Itertools;

struct Marble {
    value: u32,
    next: Option<Rc<RefCell<Marble>>>,
    previous: Weak<RefCell<Marble>>
}

struct Circle {
    current: Rc<RefCell<Marble>>
}

impl Circle {
    fn new() -> Circle {
        let zero = Rc::new(RefCell::new(Marble { 
                value: 0,
                next: None,
                previous: Weak::new()
        }));

        let one = Rc::new(RefCell::new(Marble { 
                value: 0,
                next: Some(Rc::clone(&zero)),
                previous: Rc::downgrade(&zero)
        }));

        let mut z = zero.borrow_mut();
        z.next = Some(Rc::clone(&one));
        z.previous = Rc::downgrade(&one);
        
        Circle { current: one }
    }

    fn place_next(&mut self, value: u32) {
        let marble;
        {
            let mut current = self.current.borrow_mut();
            marble = Rc::new(RefCell::new(Marble { 
                    value,
                    next: Some(Rc::clone(current.next.as_ref().unwrap())),
                    previous: Rc::downgrade(&self.current)
                    //previous: current.next.as_ref().unwrap().borrow().previous.clone()
            }));
            
            current.next.as_ref().unwrap().borrow_mut().previous = Rc::downgrade(&marble);
            current.next = Some(Rc::clone(&marble));
        }

        self.current = marble;
    }

    fn remove(&mut self) -> u32 {
        let value;
        let next;
        {
            let current = self.current.borrow();
            value = current.value;
            next = Rc::clone(current.next.as_ref().unwrap());

            current.next.as_ref().unwrap().borrow_mut().previous = current.previous.clone();
            current.previous.upgrade().unwrap().borrow_mut().next = Some(Rc::clone(current.next.as_ref().unwrap()));
        }

        self.current = next;
        value
    }

    fn move_clockwise(&mut self, steps: u32)  {
        for _ in 0..steps {
            let next = Rc::clone(self.current.borrow().next.as_ref().unwrap());
            self.current = next;
        }
    }

    fn move_counterclockwise(&mut self, steps: u32)  {
        for _ in 0..steps {
            let next = Rc::clone(&self.current.borrow().previous.upgrade().unwrap());
            self.current = next;
        }
    }

    fn play(&mut self, players: u32, marbles: u32) -> u32 {
        let mut scores: Vec<u32> = vec![0; players as usize];

        for i in 2..=marbles {
            if (i % 23) != 0 {
                self.move_clockwise(1);
                self.place_next(i);
            }
            else {
                self.move_counterclockwise(7);
                scores[(i % players) as usize] += i + self.remove();
            }
        }

        scores.iter().max().copied().unwrap()
    }
}

/*  Naive implementation I made for part 1

fn play(players: u32, marbles: u32) -> u32 {
    let mut circle: Vec<u32> = vec![0];
    let mut scores: Vec<u32> = vec![0; players as usize];
    let mut pos: usize = 1;

    for i in 1..=marbles {
        if (i % 23) != 0 {
            pos = (pos + 2) % (circle.len());
            circle.insert(pos, i);
        }
        else {
            pos = (pos + circle.len() - 7) % (circle.len());
            scores[(i % players) as usize] += i + circle.remove(pos);
        }
    }

    scores.iter().max().copied().unwrap()
}
 */

fn read_input(filename: &str) -> (u32, u32) {
    fs::read_to_string(filename)
        .unwrap()
        .split_whitespace()
        .filter_map(|s| s.parse::<u32>().ok())
        .tuples::<(u32, u32)>()
        .next()
        .unwrap()
        
}

fn part_one(players: u32, marbles: u32) -> u32 {
    let mut circle = Circle::new();
    circle.play(players, marbles)
}

fn part_two(players: u32, marbles: u32) -> u32 {
    let mut circle = Circle::new();
    circle.play(players, marbles * 100)
}

fn main() {
    let part: i32 = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let (players, marbles) = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(players, marbles))
    }
    else {
        println!("{}", part_two(players, marbles))
    }
}

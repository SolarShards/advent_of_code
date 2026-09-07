use std::env;

use std::fs::File;
use std::io::{self, BufRead};

use std::collections::HashMap;

use regex::regex;
use chrono::{NaiveDateTime, Timelike};

enum Event {
    BeginShift(u32),
    WakeUp,
    FallAsleep
}

struct GuardStats {
    total_sleep_time: u32,
    minutes: HashMap<u32, u32>,
    asleep_minute: u32
}

impl GuardStats {

    fn new() -> GuardStats {
        GuardStats { total_sleep_time: 0, minutes: HashMap::new(), asleep_minute: 0 }
    }

    fn sleep(&mut self, date: &NaiveDateTime) {
        self.asleep_minute = date.minute();
    }

    fn wake_up(&mut self, date: &NaiveDateTime) {
        self.total_sleep_time += date.minute() - self.asleep_minute;
        for i in self.asleep_minute..date.minute() {
            self.minutes.entry(i)
                        .and_modify(|e| *e += 1)
                        .or_insert(1);
        }
    }

    fn most_slept_minute(&self) -> (&u32, &u32) {
        self.minutes.iter()
                     .max_by_key(|&(_minute, occurences)| occurences)
                     .unwrap_or((&0, &0))
    }
}

fn analyse_guards(input: Vec<(NaiveDateTime, Event)>) -> HashMap<u32, GuardStats> {
    let mut stats: HashMap<u32, GuardStats> = HashMap::new();
    let mut current_guard: u32 = 0;

    for (date, event) in input {
        match event {
            Event::BeginShift(id) => {
                stats.entry(id)
                      .or_insert(GuardStats::new());
                current_guard = id;
            },
            Event::FallAsleep => {
                stats.entry(current_guard)
                      .and_modify(|g| g.sleep(&date))
                      .or_insert(GuardStats::new());
            },
            Event::WakeUp => {
                stats.entry(current_guard)
                      .and_modify(|g| g.wake_up(&date))
                      .or_insert(GuardStats::new());
            }
        }
    }

    stats
}

fn read_input(filename: &str) -> Vec<(NaiveDateTime, Event)> {
    let file = File::open(filename)
        .expect("Failed to read the file {filename}");
    let reader = io::BufReader::new(file);
    let mut events: Vec<(NaiveDateTime, Event)> = Vec::new();

    reader.lines().for_each(|line| {
        let line = line.unwrap();

        let date = NaiveDateTime::parse_from_str(
            &line[1..17],
            "%Y-%m-%d %H:%M"
        ).unwrap();

        let event = match &line[19..] {
            "falls asleep" => Event::FallAsleep,
            "wakes up" => Event::WakeUp,
            new_shift => Event::BeginShift(
                regex!(r"\d+").find(new_shift)
                              .unwrap()
                              .as_str()
                              .parse::<u32>()
                              .unwrap()
            )
        };

        events.push((date, event));
    });

    events.sort_unstable_by_key(|k| k.0);
    events
}

fn part_one(input: Vec<(NaiveDateTime, Event)>) -> u32 {
    let stats = analyse_guards(input);

    let (id, guard) = stats.iter()
                            .max_by_key(|&(_id, guard)| guard.total_sleep_time)
                            .unwrap();
    
    let (minute, _) = guard.most_slept_minute();
    id * minute
}

fn part_two(input: Vec<(NaiveDateTime, Event)>) -> u32 {
    let stats = analyse_guards(input);

    let (id, guard) = stats.iter()
                            .max_by_key(|&(_id, guard)| guard.most_slept_minute().1)
                            .unwrap();
    
    let (minute, _) = guard.most_slept_minute();
    id * minute
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

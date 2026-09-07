use std::env;
use std::fs;
use std::collections::{HashMap, HashSet, BTreeSet};

use regex::Regex;

struct Step {
    requirements: HashSet<char>,
    dependants: HashSet<char>
}

impl Step {
    fn new() -> Step {
        Step { requirements: HashSet::new(), dependants: HashSet::new() }
    }
}

struct BuildingProcess {
    steps: HashMap<char, Step>,
    ready: HashSet<char>
}

impl BuildingProcess {
    fn new(steps: HashMap<char, Step>) -> BuildingProcess {
        let ready : HashSet<char> = steps
        .iter()
        .filter_map(|(k, v)| if v.requirements.is_empty() { Some(k) } else { None })
        .copied()
        .collect();
        BuildingProcess { steps, ready }
    }

    fn ready(&self) -> &HashSet<char> {
        &self.ready
    }

    fn execute(&mut self, step: &char) {
        if self.ready.remove(step) {
            let dependants = self.steps
                .get(step)
                .unwrap()
                .dependants
                .clone();

            for d in dependants.iter() {
                if let Some(s) = self.steps.get_mut(d) {
                    s.requirements.remove(step);
                }
            }

            let unlocked: HashSet<char> = dependants
                .iter()
                .filter(|&s| self.steps
                    .get(s)
                    .unwrap_or(&Step::new())
                    .requirements
                    .is_empty()
                )
                .copied()
                .collect();

            self.ready.extend(&unlocked);
        }
    }
}

fn read_input(filename: &str) -> BuildingProcess {
    let file: String = fs::read_to_string(filename).unwrap();
    let re: Regex = Regex::new(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.").unwrap();
    let mut steps: HashMap<char, Step> = HashMap::new();

    re.captures_iter(&file).for_each(|caps| {
        let [req, step] = caps.extract().1.map(|x| x.parse::<char>().unwrap());
        steps.entry(req)
            .and_modify(|s| { s.dependants.insert(step); })
            .or_insert(Step { requirements: HashSet::new(), dependants: HashSet::from([step]) });
        steps.entry(step)
            .and_modify(|s| { s.requirements.insert(req); })
            .or_insert(Step { requirements: HashSet::from([req]), dependants: HashSet::new() });
    });

    BuildingProcess::new(steps)
}

fn part_one(mut input: BuildingProcess) -> String {

    let mut order: String = String::new();

    while let Some(step) = input.ready().iter().min().copied() {
        order.push(step);
        input.execute(&step);
    }

    order
}

fn part_two(mut input: BuildingProcess) -> u32 {

    const WORKERS: usize = 5;
    let mut total = 0;

    let mut ongoing: [Option<(char, u32)>; 5] = [None; 5];
    for (idx, &step) in (0..WORKERS).zip(input.ready()) {
        ongoing[idx] = Some((step, (step as u32) - ((b'A' - 1) as u32) + 60));
    }

    while let Some((step, duration)) = ongoing.iter().flatten().min_by_key(|(_, v)| v).copied() {

        input.execute(&step);
        total += duration;

        let mut next: BTreeSet<char> = input.ready().iter().copied().collect();

        for opt in ongoing.iter_mut() {
            if let Some((s, d)) = opt {
                if *s == step {
                    *opt = if let Some(n) = next.pop_first() {
                        Some((n, (n as u32) - ((b'A' - 1) as u32) + 60))
                    }
                    else {
                        None
                    };
                }
                else {
                    *d -= duration;
                }
            }
            else {
                *opt = if let Some(n) = next.pop_first() {
                    Some((n, (n as u32) - ((b'A' - 1) as u32) + 60))
                }
                else {
                    None
                };
            }
        }
    }

    total
}

fn main() {
    let part: i32 = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let input: BuildingProcess = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(input))
    }
    else {
        println!("{}", part_two(input))
    }
}

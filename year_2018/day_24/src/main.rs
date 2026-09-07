use std::cmp::Reverse;
use std::{env, fs, mem};
use std::collections::{HashMap, HashSet};

use regex::Regex;

#[derive(Clone)]
struct Group {
    units: u32,
    hp: u32,
    resistances: HashMap<String, u32>,
    ad: u32,
    attack_type: String,
    initiative: u32
}


fn target_selection_phase(immune_system: &HashMap<u32, Group>, infection: &HashMap<u32, Group>) -> Vec<(u32, u32)> {
    let mut allies = &immune_system;
    let mut enemies = &infection;
    let mut targeting_table: Vec<(u32, u32)> = Vec::new();
    let mut targeted: HashSet<u32> = HashSet::new();
    for _ in 0..2 {
        {
            let mut allies: Vec<(&u32, &Group)> = allies.iter().collect();
            let enemies: Vec<(&u32, &Group)> = enemies.iter().collect();
            allies.sort_by_key(|&(_, g)| Reverse((g.units * g.ad, g.initiative)));
            allies
                .iter()
                .for_each(|&(atk_id, atk_g)| {
                    let effective_power = atk_g.units * atk_g.ad;
                    if let Some((_, _, _, def_id)) = enemies
                        .iter()
                        .filter_map(|&(def_id, def_g)| {
                            let dmg = def_g.resistances.get(&atk_g.attack_type).unwrap_or(&1) * effective_power;
                            if dmg == 0 || targeted.contains(def_id) {
                                None
                            }
                            else {
                                Some((dmg, def_g.units * def_g.ad, def_g.initiative, def_id))
                            }
                        })
                        .max()
                    {
                        targeting_table.push((*atk_id, *def_id));
                        targeted.insert(*def_id);
                    }
                });
        }
        mem::swap(&mut allies, &mut enemies);
    }

    targeting_table
}

fn attack_phase(immune_system: &mut HashMap<u32, Group>, infection: &mut HashMap<u32, Group>, mut targeting_table: Vec<(u32, u32)>) -> bool {

    let mut success = false;
    targeting_table.sort_by_key(|(atk_id, _)| Reverse(immune_system.get(atk_id).unwrap_or_else(|| infection.get(atk_id).unwrap()).initiative));

    for (atk_id, def_id) in targeting_table.iter() {
        let Some(atk) = immune_system.get(atk_id).or(infection.get(atk_id)) else {continue};
        let (atk_units, atk_ad, atk_type) = (atk.units, atk.ad, atk.attack_type.clone());
        let Some(def) = immune_system.get_mut(def_id).or(infection.get_mut(def_id)) else {continue};
        let dmg = atk_units * atk_ad * def.resistances.get(&atk_type).unwrap_or(&1);
        if def.units * def.hp < dmg {
            immune_system.remove(def_id);
            infection.remove(def_id);
            success = true;
        }
        else if dmg >= def.hp {
            def.units -= dmg / def.hp;
            success = true;
        }
    }
    success
}

fn run_fight(immune_system: &mut HashMap<u32, Group>, infection: &mut HashMap<u32, Group>) -> Option<u32> {
    while immune_system.len() > 0 && infection.len() > 0 {
        let targeting_table = target_selection_phase(immune_system, infection);
        if !attack_phase(immune_system, infection, targeting_table) {
            return None;
        }
    }
    Some(immune_system.values().map(|g| g.units).sum::<u32>() + infection.values().map(|g| g.units).sum::<u32>())
}

fn read_input(filename: &str) -> (HashMap<u32, Group>, HashMap<u32, Group>) {
    let input = fs::read_to_string(filename).unwrap();
    let [a, b] = input.split("Infection").collect::<Vec<&str>>().try_into().unwrap();
    let re = Regex::new(r"(\d+) units each with (\d+) hit points(?:(?: \((.*)\) )|( ))with an attack that does (\d+) (\w+) damage at initiative (\d+)").unwrap();
    let mut id = 0u32;
    let mut teams = [a, b].iter()
        .map(|&team|
            {
                re.captures_iter(team)
                    .map(|caps| {
                        let [u, h, r, a, t, i]: [&str; 6] = caps.extract().1;
                        let units = u.parse().unwrap();
                        let hp = h.parse().unwrap();
                        let mut resistances: HashMap<String, u32> = HashMap::new();
                        let ad = a.parse().unwrap();
                        let attack_type = String::from(t);
                        let initiative = i.parse().unwrap();

                        if r != " " {
                            let r = r.chars()
                                .filter(|&c| !";,".contains(c))
                                .collect::<String>()
                                .replace(" to", "")
                                .replace(";", " ;");
                            let r = r.split(' ').collect::<Vec<&str>>();

                            [("weak", 2u32), ("immune", 0u32)]
                                .iter()
                                .for_each(|&(res, mult)| {
                                    if let Some(p) = r.iter().position(|&x| x == res) {
                                        for &token in r[(p+1)..].iter() {
                                            if ["weak", "immune"].contains(&token) {
                                                break;
                                            }
                                            resistances.insert(String::from(token), mult);
                                        }
                                    }
                                });
                        }

                        id += 1;
                        (id, Group { units, hp, resistances, ad, attack_type, initiative })
                    })
                    .collect::<HashMap<u32, Group>>()
            }
        )
        .collect::<Vec<HashMap<u32, Group>>>();

    (teams.remove(0), teams.remove(0))
}

fn part_one(mut immune_system: HashMap<u32, Group>, mut infection: HashMap<u32, Group>) -> u32 {
    run_fight(&mut immune_system, &mut infection).unwrap_or_default()
}

fn part_two(immune_system: HashMap<u32, Group>, infection: HashMap<u32, Group>) -> u32 {
    let mut boost = 0u32;
    loop {
        let mut a = immune_system.clone();
        let mut b = infection.clone();
        boost += 1;
        a.values_mut().for_each(|g| g.ad += boost);
        let Some(remaining) = run_fight(&mut a, &mut b) else { continue };
        if !a.is_empty() {
            break remaining
        }
    }
}

fn main() {
    let part: i32 = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let (immune_system, infection) = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(immune_system, infection))
    }
    else {
        println!("{}", part_two(immune_system, infection))
    }
}
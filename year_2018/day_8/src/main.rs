use std::collections::VecDeque;
use std::env;
use std::fs;

fn read_input(filename: &str) -> VecDeque<u32> {
    fs::read_to_string(filename)
        .unwrap()
        .split_whitespace()
        .map(|s| s.parse::<u32>().unwrap())
        .collect::<VecDeque<u32>>()
}

fn part_one(mut input: VecDeque<u32>) -> u32 {

    fn sum_meta(model: &mut VecDeque<u32>) -> u32 {
        let children_count = model.pop_front().unwrap();
        let metadata_count = model.pop_front().unwrap();
        let mut sum = 0;

        for _ in 0..children_count {
            sum += sum_meta(model);
        }
        for _ in 0..metadata_count {
            sum += model.pop_front().unwrap();
        }

        sum
    }

    sum_meta(&mut input)
}

fn part_two(mut input: VecDeque<u32>) -> u32 {

    struct Node {
        children: Vec<Node>,
        metadata: Vec<u32>
    }

    fn create_node(model: &mut VecDeque<u32>) -> Node {
        let children_count = model.pop_front().unwrap();
        let metadata_count = model.pop_front().unwrap();

        let mut node = Node {
            children: Vec::new(),
            metadata: Vec::new()
        };
        for _ in 0..children_count {
            node.children.push(create_node(model));
        }
        for _ in 0..metadata_count {
            node.metadata.push(model.pop_front().unwrap());
        }

        node
    }

    fn compute_node(node: &Node) -> u32{
        if node.children.is_empty() {
            node.metadata.iter().sum()
        }
        else {
            node.metadata.iter().map(|i: &u32| {
                let i: usize = *i as usize;
                if (1..=node.children.len()).contains(&i) {
                    compute_node(&node.children[i-1])
                }
                else {
                    0
                }
            }).sum()
        }
    }

    let root = create_node(&mut input);

    compute_node(&root)
}

fn main() {
    let part: i32 = env::args().nth(1).unwrap().parse::<i32>().unwrap();
    let input: VecDeque<u32> = read_input("input.txt");
    if part == 1 {
        println!("{}", part_one(input))
    }
    else {
        println!("{}", part_two(input))
    }
}

pub struct Knapsack {
    size: usize,

    items: Vec<Item>,
}

struct Item {
    value: u32,
    weight: u32,
}

pub type KnapsackSolution = Vec<Vec<u32>>;

pub fn knapsack(problem: &Knapsack) -> KnapsackSolution {
    let item_count = problem.items.len();
    let mut solution = vec![vec![0; problem.size + 1]; item_count + 1];

    for i in 0..item_count + 1 {
        for j in 0..problem.size + 1 {
            if i == 0 || j == 0 {
                solution[i][j] = 0;
            } else if problem.items[i - 1].weight as usize <= j {
                solution[i][j] = std::cmp::max(
                    problem.items[i - 1].value
                        + solution[i - 1][j - problem.items[i - 1].weight as usize],
                    solution[i - 1][j],
                );
            } else {
                solution[i][j] = solution[i - 1][j];
            }
        }
    }

    solution
}

pub fn read_file(path: &str) -> Knapsack {
    let mut file = std::fs::File::open(path).expect("file not found");
    let mut contents = String::new();
    std::io::Read::read_to_string(&mut file, &mut contents)
        .expect("something went wrong reading the file");

    let mut lines = contents.lines();
    let mut first_line = lines.next().unwrap().split_whitespace();
    let size = first_line.next().unwrap().parse::<usize>().unwrap();
    let item_count = first_line.next().unwrap().parse::<usize>().unwrap();
    let mut items = Vec::with_capacity(item_count);

    for line in lines {
        let mut parts = line.split_whitespace();
        let value = parts.next().unwrap().parse::<u32>().unwrap();
        let weight = parts.next().unwrap().parse::<u32>().unwrap();
        items.push(Item { value, weight });
    }

    Knapsack { size, items }
}

pub fn optimal_solution(solution: &KnapsackSolution) -> usize {
    *solution.last().unwrap().last().unwrap() as usize
}

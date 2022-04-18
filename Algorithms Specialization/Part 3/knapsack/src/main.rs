use knapsack::*;

fn main() {
    println!("Knapsack problem solution for: knapsack1.txt");
    println!("Reading File...");
    let problem = read_file("knapsack1.txt");
    println!("Solving...");
    let solution = knapsack(&problem);
    println!("Optimal solution: {}", optimal_solution(&solution));

    println!("Knapsack problem solution for: knapsack_big.txt");
    println!("Reading File...");
    let problem = read_file("knapsack_big.txt");
    println!("Solving...");
    let solution = knapsack_slick(&problem);
    println!("Optimal solution: {}", optimal_solution(&solution));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_file() {
        read_file("knapsack1.txt");
    }

    fn test_complete(path: &str, expected: usize) {
        let data = read_file(path);
        let solution = knapsack(&data);
        let solution2 = knapsack_slick(&data);
        assert_eq!(optimal_solution(&solution), expected);
        assert_eq!(optimal_solution(&solution2), expected);
    }

    #[test]
    fn input_random_5() {
        test_complete("input_random_5_10_10.txt", 14);
    }

    #[test]
    fn input_random_17() {
        test_complete("input_random_17_100_1000.txt", 1993);
    }

    #[test]
    fn input_random_26() {
        test_complete("input_random_26_1000_1000.txt", 18669);
    }
}

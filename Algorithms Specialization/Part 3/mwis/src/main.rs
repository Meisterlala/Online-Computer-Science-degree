use mwis::*;

fn main() {
    let filename = "mwis.txt";
    println!("Parsing file {}", filename);
    let graph = read_file(filename);
    println!("Finding max weight");
    let (max_weight, _weights, path) = mwis(&graph);
    println!("Max weight: {}", max_weight);
    let solution = asked(&path);
    println!("Included Vertices: {:?}", solution);
}

fn read_file(path: &str) -> PathGraph {
    use std::io::BufRead;

    // Read File
    let file = std::fs::File::open(path).unwrap();
    let reader = std::io::BufReader::new(file);
    let mut lines = reader.lines();

    // Parse File
    let number_of_vertices = lines.next().unwrap().unwrap().parse::<usize>().unwrap();

    let mut graph = Vec::with_capacity(number_of_vertices);
    for line in lines {
        let line = line.unwrap();
        let weight = line.parse::<usize>().unwrap();
        graph.push(weight);
    }

    // Assert correct number of vertices
    assert_eq!(graph.len(), number_of_vertices);

    graph
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn input_random_9() {
        let graph = read_file("input_random_9_40.txt");
        let (_, _, path) = mwis(&graph);
        let solution = asked(&path);
        assert_eq!(
            solution,
            [false, true, false, true, false, false, false, false]
        );
    }
    #[test]
    fn input_random_10() {
        let graph = read_file("input_random_10_40.txt");
        let (_, _, path) = mwis(&graph);
        let solution = asked(&path);
        assert_eq!(
            solution,
            [true, false, false, true, false, false, false, false]
        );
    }
    #[test]
    fn input_random_11() {
        let graph = read_file("input_random_11_40.txt");
        let (_, _, path) = mwis(&graph);
        let solution = asked(&path);
        assert_eq!(
            solution,
            [true, false, true, false, true, false, false, false]
        );
    }
    #[test]
    fn input_random_12() {
        let graph = read_file("input_random_12_40.txt");
        let (_, _, path) = mwis(&graph);
        let solution = asked(&path);
        assert_eq!(
            solution,
            [false, true, false, true, true, false, false, false]
        );
    }
    #[test]
    fn input_random_36() {
        let graph = read_file("input_random_36_2000.txt");
        let (_, _, path) = mwis(&graph);
        let solution = asked(&path);
        assert_eq!(
            solution,
            [false, true, false, true, false, true, false, false]
        );
    }

    #[test]
    fn input_random_37() {
        let graph = read_file("input_random_37_4000.txt");
        let (_, _, path) = mwis(&graph);
        let solution = asked(&path);
        assert_eq!(
            solution,
            [true, false, true, false, false, false, true, false]
        );
    }
}

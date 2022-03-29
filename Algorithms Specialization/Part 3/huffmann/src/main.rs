use huffmann::*;

fn main() {
    println!("Parsing File");
    let weights = read_file("huffman.txt".into());
    println!("Calculation optimal Huffman compression");
    let tree = compact(weights);
    println!("Maximal lenght of a symbol: {}", max(&tree));
    println!("Minimal lenght of a symbol: {}", min(&tree));

    _write_graph(
        &compact(read_file("huffman.txt".into())),
        "huffman.dot".into(),
    );
}

// Tests
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn open_file() {
        read_file("input_random_10_40.txt".into());
        read_file("huffman.txt".into());
    }

    #[test]
    fn input_random_5() {
        let weights = read_file("input_random_5_20.txt".into());
        let tree = compact(weights);

        assert_eq!(max(&tree), 6);
        assert_eq!(min(&tree), 4);
    }

    #[test]
    fn input_random_10() {
        let weights = read_file("input_random_10_40.txt".into());
        let tree = compact(weights);
        assert_eq!(max(&tree), 9);
        assert_eq!(min(&tree), 4);
    }

    #[test]
    fn input_random_45() {
        let weights = read_file("input_random_45_10000.txt".into());
        let tree = compact(weights);

        assert_eq!(max(&tree), 24);
        assert_eq!(min(&tree), 12);
    }

    #[test]
    fn input_picked_10() {
        let weights = read_file("input_picked_10.txt".into());
        let tree = compact(weights);

        assert_eq!(max(&tree), 5);
        assert_eq!(min(&tree), 2);
    }

    #[test]
    fn input_picked_15() {
        let weights = read_file("input_picked_15.txt".into());
        let tree = compact(weights);

        assert_eq!(max(&tree), 6);
        assert_eq!(min(&tree), 3);
    }
}

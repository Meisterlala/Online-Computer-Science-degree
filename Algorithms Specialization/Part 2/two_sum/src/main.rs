use std::collections::HashSet;

// Given as input:
// unsorted Array of Integers and Target sum T
// Goal:
// determine if there are 2 numbers in the Array, which satisfy x+y=T

fn main() {
    // Start Time
    let start = std::time::Instant::now();

    println!("Reading 2sum.txt");
    // Read Array
    let input = read_array("2sum.txt");

    // Insert Element into Hashtable
    println!("Creating Hashtable");
    let mut hashtable = HashSet::with_capacity(input.len() + 8);
    //let mut hashtable = HashSet::with_capacity_and_hasher(input.len() + 8, MyHasher { state: 0 });
    for i in 0..input.len() {
        hashtable.insert(input[i]);
    }
    println!(
        "Hashtable created with {} distinct Entries",
        hashtable.len()
    );

    // for each x in Array, Lookup T-X in Hashtable
    println!("Searching for pairs");
    let mut count: usize = 0;
    for t in -10000..=10000 {
        for i in 0..input.len() {
            let x = input[i];
            let y = t - x;

            // Check for Distinct Pairs
            if x == y {
                continue;
            }

            if hashtable.contains(&y) {
                // Report X,Y
                println!("{: >15}  + {: >15} = {: >10}", x, y, t);
                count += 1;
                break;
            }
        }
    }
    // Report Count
    println!(
        "Found {} value pairs for target values in the intervall [-10000,10000]",
        count
    );

    // Report Time
    let duration = start.elapsed();
    println!("Took: {}s", duration.as_secs());
}

fn read_array(filename: &str) -> Vec<isize> {
    use std::fs::File;
    use std::io::Read;

    let mut f = File::open(filename).expect("file not found");
    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("something went wrong reading the file");
    let mut input: Vec<isize> = Vec::new();
    for line in contents.lines() {
        input.push(line.parse::<isize>().unwrap());
    }
    input
}

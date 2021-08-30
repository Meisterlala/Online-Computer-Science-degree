use std::fs;
use std::time::Instant;

const DATA_PATH: &str = "IntegerArray.txt";

fn main() {
    println!("Reading File: {}", DATA_PATH);
    let content = read_array(DATA_PATH);
    println!("Counting Inversions ...");
    let start_time = Instant::now();
    let count = inversions(content);
    let elapsed_time = start_time.elapsed();
    println!("Found Inversions: {}", count);
    println!(
        "Count took  {}ms",
        elapsed_time.as_millis()
    );
}

pub fn inversions(array: Vec<i32>) -> u32 {
    let (_, count) = inversions_sorted(&array);
    return count;
}

fn inversions_sorted(array: &[i32]) -> (Vec<i32>, u32) {
    // Base case
    let len = array.len();
    if len <= 1 {
        return (array.to_vec(), 0);
    };

    // Recusivly Count Left, Right and Split Inversion
    let split_point: usize = len / 2;
    let (left, left_c) = inversions_sorted(&array[..split_point]);
    let (right, right_c) = inversions_sorted(&array[split_point..]);
    let (sorted, split_c) = inversions_split(&left, &right);

    // Add recusivly calculated values and return
    return (sorted, left_c + right_c + split_c);
}

fn inversions_split(left: &[i32], right: &[i32]) -> (Vec<i32>, u32) {
    let mut sorted: Vec<i32> = vec![];
    let mut inversions: u32 = 0;
    let mut left_index = 0;
    let mut right_index = 0;

    let left_len = left.len();
    let right_len = right.len();

    for _ in 0..(left_len + right_len) {
        // Check index
        let left_oob = left_index > (left_len - 1);
        let right_oob = right_index > (right_len - 1);
        if left_oob {
            sorted.push(right[right_index]);
            right_index += 1;
            continue;
        }
        if right_oob {
            sorted.push(left[left_index]);
            left_index += 1;
            continue;
        }
        if left_oob && right_oob {
            break;
        }

        // Compare
        if left[left_index] < right[right_index] {
            sorted.push(left[left_index]);
            left_index += 1;
        } else {
            sorted.push(right[right_index]);
            right_index += 1;
            // Count Inversions
            inversions += (left_len - left_index) as u32;
        }
    }

    return (sorted, inversions);
}

fn read_array(path: &str) -> Vec<i32> {
    // Read File
    let content = fs::read_to_string(path).expect("Could not read file: {}");
    // Split String per Line
    let split = content
        .split_whitespace()
        .map(|s| s.trim())
        .collect::<Vec<&str>>();
    // Convert to int
    let mut result: Vec<i32> = vec![];
    for s in split {
        match s.parse() {
            Ok(i) => result.push(i),
            Err(_) => println!("Could not convert {} to i32", s),
        }
    }
    return result;
}

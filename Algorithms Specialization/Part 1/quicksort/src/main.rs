use rand::prelude::*;
use std::{mem::swap, time::Instant};

fn main() {
    let array_size = 1000000;
    println!("Generating array of size {}", array_size);
    let mut input = generate_array(array_size);
    let mut input_copy = input.clone();
    let mut input_copy2 = input.clone();
    println!("Sorting... ");

    // Sort
    let start_time = Instant::now();
    quick_sort(&mut input);
    let elapsed = start_time.elapsed().as_millis();

    // Count Amount of Errors
    let errors = input
        .windows(3)
        .filter(|w| w[0] > w[1] || w[1] > w[2])
        .count();
    match errors {
        e if e > 0 => println!("ERROR {} mismatches", e),
        _ => println!("OK"),
    }

    println!("");
    println!("My sorting took {}ms", elapsed);

    // Time default Sort
    let start_time = Instant::now();
    input_copy.sort();
    let elapsed = start_time.elapsed().as_millis();
    println!("Default sorting took {}ms", elapsed);

    // Time default Sort
    let start_time = Instant::now();
    input_copy2.sort_unstable();
    let elapsed = start_time.elapsed().as_millis();
    println!("Unstable sorting took {}ms", elapsed);
}

fn generate_array(length: isize) -> Vec<isize> {
    let mut nums: Vec<isize> = (1..=length).collect();
    nums.shuffle(&mut rand::thread_rng());
    nums
}

pub fn quick_sort(array: &mut [isize]) {
    let mut random = thread_rng();
    let l = array.len();
    quick_sort_cached(array, l, &mut random);

    fn quick_sort_cached(array: &mut [isize], length: usize, rng: &mut ThreadRng) {
        if length <= 1 {
        } else {
            let pivot = partition_random(array, length, rng);
            quick_sort_cached(&mut array[..pivot], pivot, rng);
            quick_sort_cached(&mut array[pivot..], length - pivot, rng);
        }
    }

    fn partition_random(array: &mut [isize], length: usize, rng: &mut ThreadRng) -> usize {
        // Chooses pivot randomly and move to first index
        // Can be made faster by caching rng
        let pivot_index = rng.gen_range(0..length);
        let mut pivot = array[0];
        swap(&mut array[0], &mut pivot);
        partition(array, length)
    }

    fn partition(array: &mut [isize], length: usize) -> usize {
        let pivot = array[0];
        let mut i = 1;
        // For every element in array
        for j in 1..length {
            // Swap if value less than the pivot
            if array[j] < pivot {
                array.swap(j, i);
                i += 1;
            }
        }
        // Swap first element with pivot
        array.swap(0, i - 1);
        i
    }
}

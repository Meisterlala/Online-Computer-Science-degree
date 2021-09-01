#![feature(test)]

use rand::prelude::*;
use std::{mem::swap, time::Instant};
use quicksort::quick_sort;

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
    print!("Checking result... ");
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


use criterion::{black_box, criterion_group, criterion_main, Criterion};
use quicksort::quick_sort;

use rand::prelude::*;

fn test_sort(c: &mut Criterion) {
    let mut input = generate_array(1000);

    c.bench_function("quicks", |b| {
        b.iter(|| {
            let mut clone = input.clone();
            quick_sort(&mut clone);
        })
    });
}

fn generate_array(length: isize) -> Vec<isize> {
    let mut nums: Vec<isize> = (1..=length).collect();
    nums.shuffle(&mut rand::thread_rng());
    nums
}

criterion_group!(benches, test_sort);
criterion_main!(benches);

use criterion::{criterion_group, criterion_main, Criterion};
use knapsack::*;

pub fn benchmark_big(c: &mut Criterion) {
    let mut group = c.benchmark_group("Knapsack big");
    group.sample_size(10);

    let problem = read_file("knapsack_big.txt");

    group.bench_function("normal", |b| {
        b.iter(|| {
            let _solution = knapsack(&problem);
        })
    });

    group.bench_function("slick", |b| {
        b.iter(|| {
            let _solution = knapsack_slick(&problem);
        })
    });

    group.finish();
}

pub fn benchmark_small(c: &mut Criterion) {
    let mut group = c.benchmark_group("Knapsack small");
    group.measurement_time(std::time::Duration::from_secs(15));

    let problem = read_file("knapsack1.txt");

    group.bench_function("normal", |b| {
        b.iter(|| {
            let _solution = knapsack(&problem);
        })
    });

    group.bench_function("slick", |b| {
        b.iter(|| {
            let _solution = knapsack_slick(&problem);
        })
    });

    group.finish();
}

criterion_group!(benches, benchmark_small, benchmark_big);
criterion_main!(benches);

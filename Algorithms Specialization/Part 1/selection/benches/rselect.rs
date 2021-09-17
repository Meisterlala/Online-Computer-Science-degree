use criterion::{black_box, criterion_group, criterion_main, Criterion};
use selection::rselect;

pub fn bench_rselect(c: &mut Criterion){
    let random: Vec<isize> = std::iter::repeat_with(|| fastrand::isize(0..1000))
        .take(1000)
        .collect();
    
    c.bench_function("rselect 1000", |b| b.iter(|| rselect(black_box(&random), black_box(2))));
}


criterion_group!(benches, bench_rselect);
criterion_main!(benches);
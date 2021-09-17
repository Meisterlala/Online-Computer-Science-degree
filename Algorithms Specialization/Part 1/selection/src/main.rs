use selection::rselect;

fn main() {

    let random: Vec<isize> = std::iter::repeat_with(|| fastrand::isize(0..1000))
        .take(100)
        .collect();

    println!("Array: {:?}", random);
    let res = rselect(&random, 6);
    println!("6st Smallest Element: {:?}", res);
}

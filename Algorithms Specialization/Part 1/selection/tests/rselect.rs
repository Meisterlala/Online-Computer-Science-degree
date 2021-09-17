use selection::rselect;

#[test]
fn smallest() {
    let random: Vec<isize> = std::iter::repeat_with(|| fastrand::isize(0..1000))
        .take(100)
        .collect();

    let correct = *random.iter().min().expect("Not Found");
    let res = rselect(&random, 1);
    assert_eq!(correct, res);
}

#[test]
fn third() {
    let mut v: Vec<isize> = vec![-4, -2, 1, 5, 20, 18412];
    fastrand::shuffle(&mut v);

    assert_eq!(rselect(&v, 3), 1);
}

#[test]
fn last() {
    let mut v: Vec<isize> = vec![-4, -2, 1, 5, 20, 18412];
    fastrand::shuffle(&mut v);

    assert_eq!(rselect(&v, 6), 18412);
}

#[test]
fn multible() {
    let mut v: Vec<isize> = vec![-4, -4, -4, -3, -3, 2, 0, 4];
    fastrand::shuffle(&mut v);

    assert_eq!(rselect(&v, 1), -4);
    assert_eq!(rselect(&v, 3), -4);
    assert_eq!(rselect(&v, 4), -3);
}

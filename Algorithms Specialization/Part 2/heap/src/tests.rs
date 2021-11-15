#[allow(unused_imports)]
use crate::Heap;

#[test]
fn insert() {
    let mut h = Heap::<u32>::new();
    h.insert(3);
    h.insert(4);
    h.insert(2);
}

#[test]
fn min() {
    let mut h = Heap::<u32>::new();
    h.insert(3);
    h.insert(4);
    h.insert(2);

    assert_eq!(h.min(), Some(2));
    assert_eq!(h.min(), Some(3));
    assert_eq!(h.min(), Some(4));
    assert_eq!(h.min(), None);
}

#[test]
fn len() {
    let mut h = Heap::<u32>::new();
    h.insert(3);
    h.insert(4);
    h.insert(2);

    assert_eq!(h.len(), 3);
}

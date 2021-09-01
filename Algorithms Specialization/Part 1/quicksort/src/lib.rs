use rand::prelude::*;
use std::{mem::swap, time::Instant};

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
        /*
            let pivot_index = rng.gen_range(0..length);
            let mut pivot = array[0];
            swap(&mut array[0], &mut pivot);
        */
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

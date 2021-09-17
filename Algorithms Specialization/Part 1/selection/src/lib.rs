fn random_selection(array: &mut [isize], array_length: usize, index: usize) -> isize {
    if array_length == 1 {
        array[0]
    } else {
        let partition_index = partition_random(array, array_length);
        if partition_index > index {
            // Is in left side of array
            random_selection(&mut array[0..partition_index], partition_index, index)
        } else if partition_index < index {
            // is in right side of array
            random_selection(
                &mut array[partition_index..],
                array_length - partition_index,
                index - partition_index,
            )
        } else {
            array[partition_index]
        }
    }
}

fn partition_random(array: &mut [isize], length: usize) -> usize {
    let pivot_index = fastrand::usize(0..length);
    array.swap(0, pivot_index);

    let pivot = array[0];
    let mut i = 1;
    // For every element in array
    for j in 1..length {
        // Swap if value less than the pivot
        if array[j] <= pivot {
            array.swap(j, i);
            i += 1;
        }
    }
    // Swap first element with pivot
    array.swap(0, i - 1);
    i - 1
}
/// Selects the n'th smallest element in the array
pub fn rselect(array: &Vec<isize>, n: usize) -> isize {
    let mut input = array.clone();
    let len = array.len();
    random_selection(input.as_mut_slice(), len, n - 1)
}

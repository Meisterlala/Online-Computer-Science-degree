use text_io::read;

fn main() {
    println!("Hello, world!");

    let line: String = read!("{}\n");
    // Create input Vec by mapping the parse
    let array: Vec<i32> = line
        .split_whitespace()
        .map(|s| s.parse::<i32>().unwrap())
        .collect();

    println!("Unsorted: {:?}", array);
    let sorted = mergesort(array);
    println!("Sorted {:?}", sorted);
}

#[test]
fn merge_test() {
    assert_eq!(
        mergesort(vec![1, 6, 2, 5, 4, 3, 8, 7, 9]),
        vec![1, 2, 3, 4, 5, 6, 7, 8, 9]
    );
}

#[inline]
pub fn mergesort(mut array: Vec<i32>) -> Vec<i32> {
    // Base Case
    if array.len() == 2 {
        if array[0] < array[1] {
            return array;
        } else {
            return vec![array[1], array[0]];
        }
    } else if array.len() == 1 {
        return array;
    };

    // Recursivly Sort
    let split = array.len() / 2;
    let left = mergesort(array[0..split].to_vec());
    let right = mergesort(array[split..].to_vec());

    // Merge
    let mut ri = 0;
    let mut li = 0;

    for k in 0..array.len() {
        // Out of Bound Checks
        let left_oob = li > (left.len() - 1);
        let right_oob = ri > (right.len() - 1);
        if left_oob {
            array[k] = right[ri];
            ri += 1;
            continue;
        } else if right_oob {
            array[k] = left[li];
            li += 1;
            continue;
        }
        if left_oob && right_oob {
            break;
        }

        // Compare
        if left[li] < right[ri] {
            array[k] = left[li];
            li += 1;
        } else {
            array[k] = right[ri];
            ri += 1;
        }
    }

    // Return Sorted
    return array;
}

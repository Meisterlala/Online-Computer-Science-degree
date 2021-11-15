mod tests;

pub struct Heap<T> {
    items: Vec<T>,
}

impl<T: std::cmp::PartialOrd> Heap<T> {
    pub fn new() -> Self {
        Heap { items: vec![] }
    }

    /// Insert a new Item
    ///
    /// Running time: **O(log n)**
    pub fn insert(self: &mut Self, item: T) {
        self.items.push(item);

        if self.items.len() < 2 {
            return;
        }

        let mut inserted_index = self.items.len() - 1;
        let mut parent = Heap::<T>::parent(inserted_index);
        while self.items[parent] > self.items[inserted_index] {
            self.swap(parent, inserted_index);
            inserted_index = parent;
            parent = Heap::<T>::parent(self.items.len());
        }
    }

    /// Return the minimum of the heap and remove it
    ///
    /// Returns none if heap is empty
    ///
    /// Running time: **O(log n)**
    pub fn min(self: &mut Self) -> Option<T> {
        if self.items.len() == 0 {
            return None;
        }

        self.swap(0, self.items.len() - 1);
        let res = self.items.pop().unwrap();

        let mut b_inded = 0;
        let (mut left, mut right) = Heap::<T>::children(b_inded);
        while self.items[left] < self.items[b_inded] || self.items[right] < self.items[b_inded] {
            if self.items[left] < self.items[right] {
                self.swap(left, b_inded);
                b_inded = left;
            } else {
                self.swap(right, b_inded);
                b_inded = right;
            }

            let (l, r) = Heap::<T>::children(b_inded);
            left = l;
            right = r;
        }

        Some(res)
    }

    /// Amount of Items
    pub fn len(self: Self) -> usize {
        self.items.len()
    }

    fn swap(self: &mut Self, a: usize, b: usize) {
        self.items.swap(a, b);
    }

    fn parent(index: usize) -> usize {
        (index / 2) - 1
    }

    fn children(index: usize) -> (usize, usize) {
        let index_2 = index * 2;
        (index_2, index_2 + 1)
    }
}

impl<T: std::cmp::PartialOrd> Default for Heap<T> {
    fn default() -> Self {
        Self::new()
    }
}

#![allow(unused)]

pub struct Union {
    data: Vec<usize>,
}

impl Union {
    pub fn initilize(size: usize) -> Self {
        let mut data = vec![];

        for i in 0..=size {
            data.push(i);
        }

        Union { data }
    }

    /// Return Set of Node
    pub fn find(&self, from: usize) -> usize {
        self.data[from]
    }

    /// Merge a into b
    pub fn union(&mut self, a: usize, b: usize) {
        let target = self.data[a];
        for i in 0..self.data.len() {
            if self.data[i] == target {
                self.data[i] = self.data[b];
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple() {
        let mut union = Union::initilize(2);
        union.union(0, 1);
        assert_eq!(union.find(0), 1);
    }

    #[test]
    fn test_simple2() {
        let mut union = Union::initilize(5);
        union.union(0, 1);
        union.union(2, 1);
        union.union(3, 4);
        union.union(4, 1);

        assert_eq!(union.find(0), 1);
        assert_eq!(union.find(1), 1);
        assert_eq!(union.find(2), 1);
        assert_eq!(union.find(3), 1);
        assert_eq!(union.find(4), 1);
    }

    #[test]
    fn test_simple3() {
        let mut union = Union::initilize(5);
        union.union(0, 1);
        union.union(2, 1);
        union.union(3, 4);
        union.union(4, 1);
        union.union(0, 2);
        union.union(0, 3);
        union.union(0, 4);

        assert_eq!(union.find(0), union.find(1));
        assert_eq!(union.find(0), union.find(2));
        assert_eq!(union.find(0), union.find(3));
        assert_eq!(union.find(0), union.find(4));
    }

    #[test]
    fn test_simple4() {
        let mut union = Union::initilize(5);
        union.union(0, 1);
        union.union(2, 1);
        union.union(3, 4);
        union.union(4, 1);
        union.union(0, 2);
        union.union(0, 3);
        union.union(0, 4);
        union.union(1, 2);
        union.union(1, 3);
        union.union(1, 4);

        assert_eq!(union.find(0), union.find(1));
        assert_eq!(union.find(0), union.find(2));
        assert_eq!(union.find(0), union.find(3));
        assert_eq!(union.find(0), union.find(4));
    }
}

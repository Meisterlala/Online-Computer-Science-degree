#[derive(Debug)]
pub struct BTree {
    pub freq: usize,
    pub zero: Option<Box<BTree>>,
    pub one: Option<Box<BTree>>,
}

impl BTree {
    pub fn new(freq: usize) -> Self {
        BTree {
            freq,
            zero: None,
            one: None,
        }
    }

    pub fn min_height(&self) -> usize {
        let mut min = 0;
        if let Some(ref zero) = self.zero {
            min = zero.min_height();
        }
        if let Some(ref one) = self.one {
            min = min.min(one.min_height());
        }
        min + 1
    }

    pub fn max_height(&self) -> usize {
        let mut max = 0;
        if let Some(ref zero) = self.zero {
            max = zero.max_height();
        }
        if let Some(ref one) = self.one {
            max = max.max(one.max_height());
        }
        max + 1
    }
}

impl std::cmp::Ord for BTree {
    fn cmp(&self, other: &BTree) -> std::cmp::Ordering {
        self.freq.cmp(&other.freq)
    }
}

impl std::cmp::PartialOrd for BTree {
    fn partial_cmp(&self, other: &BTree) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl std::cmp::PartialEq for BTree {
    fn eq(&self, other: &BTree) -> bool {
        self.freq == other.freq
    }
}

impl std::cmp::Eq for BTree {}

impl Default for BTree {
    fn default() -> Self {
        Self::new(0)
    }
}

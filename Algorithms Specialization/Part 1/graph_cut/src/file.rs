use petgraph::Undirected;

pub struct GraphFile {
    content: Vec<String>,
    next_line: usize,
}

impl Iterator for GraphFile {
    type Item = (usize, Vec<usize>);

    fn next(&mut self) -> Option<Self::Item> {
        // If reached last line in array
        if self.next_line >= self.content.len() {
            return None;
        }

        let line = &self.content[self.next_line];
        let mut split: Vec<&str> = line.split(char::is_whitespace).collect();

        // remove last empy
        split.pop();

        // If last or invalid
        if split.len() < 2 {
            return None;
        }

        // Index of Node
        let index: usize = split[0].parse().ok()?;
        let index = index - 1;

        let mut edges: Vec<usize> = Vec::new();
        for connected_with in split[1..].to_vec() {
            let i: usize = connected_with.parse().ok()?;
            let i = i - 1;
            edges.push(i);
        }

        self.next_line += 1;

        Some((index, edges))
    }
}

impl GraphFile {
    pub fn new(path: &str) -> Option<Self> {
        if let Ok(content) = std::fs::read_to_string(path) {
            let mut vec: Vec<String> = Vec::new();
            for line in content.lines() {
                vec.push(String::from(line));
            }

            Some(GraphFile {
                content: vec,
                next_line: 0,
            })
        } else {
            None
        }
    }

    pub fn to_graph(&mut self) -> petgraph::Graph<usize, usize, Undirected, usize> {
        use petgraph::graph::Graph;

        let mut g = Graph::<usize, usize, Undirected, usize>::default();

        // Add Nodes
        for (index, edges) in self {
            let index_iter = std::iter::repeat(index);
            let combined_iter = index_iter.zip(edges);
            let edges: Vec<(usize, usize)> = combined_iter.collect();
            // println!("{:?}", &edges);
            g.extend_with_edges(&edges)
        }

        g
    }
}

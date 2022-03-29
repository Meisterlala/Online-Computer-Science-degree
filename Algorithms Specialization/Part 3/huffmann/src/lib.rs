mod tree;

use std::cmp::Reverse;
use std::collections::BinaryHeap;
use tree::*;

pub fn compact(weights: Vec<usize>) -> BTree {
    // Create Nodes
    let mut min_heap = BinaryHeap::new();
    for weight in weights {
        min_heap.push(Reverse(BTree::new(weight)));
    }

    // Merge Nodes until there are only 2
    while min_heap.len() > 1 {
        // The 2 nodes, with the lowest frequency, are merged
        let Reverse(left) = min_heap.pop().unwrap();
        let Reverse(right) = min_heap.pop().unwrap();

        // The new node is created
        let mut merged = BTree::new(left.freq + right.freq);
        merged.zero = Some(Box::new(left));
        merged.one = Some(Box::new(right));

        // Add new node
        min_heap.push(Reverse(merged));
    }

    let Reverse(tree) = min_heap.pop().unwrap();
    tree
}

pub fn min(tree: &BTree) -> usize {
    tree.min_height() - 1
}

pub fn max(tree: &BTree) -> usize {
    tree.max_height() - 1
}

pub fn read_file(path: String) -> Vec<usize> {
    use std::fs::File;
    use std::io::prelude::*;
    use std::io::BufReader;

    let file = File::open(path).expect("file not found");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    let mut weights = Vec::new();

    let node_count = lines.next().unwrap().unwrap().parse::<usize>().unwrap();

    for line in lines {
        let line = line.unwrap();
        let mut parts = line.split_whitespace();
        let weight = parts.next().unwrap().parse::<usize>().unwrap();
        weights.push(weight);
    }

    assert!(weights.len() == node_count);

    weights
}

use petgraph::graph::Graph;
use petgraph::graph::NodeIndex;
/// Only used for visualisation
fn _create_graph(tree: &BTree, graph: &mut Graph<usize, usize>, root: NodeIndex) {
    if let Some(ref zero) = tree.zero {
        if zero.one != None && zero.zero != None {
            let zero_index = graph.add_node(0);
            graph.add_edge(root, zero_index, 0);
            _create_graph(zero, graph, zero_index);
        } else {
            let zero_index = graph.add_node(zero.freq);
            graph.add_edge(root, zero_index, 0);
            _create_graph(zero, graph, zero_index);
        }
    }
    if let Some(ref one) = tree.one {
        if one.one != None && one.zero != None {
            let one_index = graph.add_node(0);
            graph.add_edge(root, one_index, 1);
            _create_graph(one, graph, one_index);
        } else {
            let one_index = graph.add_node(one.freq);
            graph.add_edge(root, one_index, 1);
            _create_graph(one, graph, one_index);
        }
    }
}

pub fn _write_graph(tree: &BTree, path: String) {
    use petgraph::dot::*;
    use std::fs::*;

    let mut graph = Graph::<usize, usize>::new();
    let root = graph.add_node(0);
    _create_graph(tree, &mut graph, root);

    let data = Dot::with_config(&graph, &[]);
    write(path, format!("{:?}", data)).unwrap()
}

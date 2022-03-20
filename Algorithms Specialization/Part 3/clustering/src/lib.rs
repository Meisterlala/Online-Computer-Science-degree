#![allow(unused)]

mod union;

use petgraph::visit::*;
use petgraph::*;
use union::*;
use std::collections::HashSet;

pub type G = Graph<(), u32, Undirected, usize>;

/// Return clusterd Graph and spacing
pub fn clustering(graph: &G, k: u32) -> (G, u32) {
    // return Graph
    let mut result = G::with_capacity(graph.node_count(), 1000);

    // Sort all Edges by weight
    let mut sorted: Vec<_> = graph.edge_references().collect();
    sorted.sort_by(|a, b| a.weight().cmp(b.weight()));

    // Union-Find
    let mut union = Union::initilize(graph.node_count());

    // Iterate until target reached
    let mut edge_index = 0;
    let mut cluster_count = graph.node_count();
    while edge_index < sorted.len() {
        let edge = sorted[edge_index];
        let source = edge.source().index();
        let target = edge.target().index();

        // if no cycles
        if union.find(source) != union.find(target) {
            // Break after reaching k
            if cluster_count == k as usize {
                return (result, *edge.weight());
            }

            // Add to Graph
            result.extend_with_edges(&[(edge.source(), edge.target(), *edge.weight())]);
            // Update Union
            union.union(source, target);

            cluster_count -= 1;
        }

        edge_index += 1;
    }

    panic!("No Solution");
}


pub fn max_weight(graph: &G) -> u32 {
    *graph.edge_weights().max().unwrap_or(&0)
}

pub fn read_file(path: &str) -> Result<G, Box<dyn std::error::Error>> {
    let file = std::fs::read_to_string(path)?;
    let mut lines = file.lines();
    let node_count = lines
        .next()
        .ok_or("Error reading first line")?
        .parse::<usize>()?;

    let mut graph = G::with_capacity(node_count, node_count * 2);

    // For each line in File
    for line in lines {
        // Skip empty lines
        if line.is_empty() {
            continue;
        }
        let mut split = line.split_whitespace();
        let node1 = split
            .next()
            .ok_or("first node not defined")?
            .parse::<usize>()?
            - 1;
        let node2 = split
            .next()
            .ok_or("second node not defined")?
            .parse::<usize>()?
            - 1;
        let edge_cost = split
            .next()
            .ok_or("edge cost not defined")?
            .parse::<u32>()?;
        graph.extend_with_edges(&[(node1, node2, edge_cost)]);
    }

    Ok(graph)
}

pub fn write_graph(graph: &G, path: &str) {
    use petgraph::dot::*;
    use std::fs::*;

    let data = Dot::with_config(graph, &[Config::NodeNoLabel]);
    let x = write(path, format!("{:?}", data));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_simple() {
        assert_eq!(read_file("clustering_small.txt").unwrap().node_count(), 7);
        assert_eq!(read_file("clustering1.txt").unwrap().node_count(), 500);

        assert_eq!(read_file("random_1.txt").unwrap().node_count(), 8);
        assert_eq!(read_file("random_1.txt").unwrap().edge_count(), 28);

        assert_eq!(read_file("random_11.txt").unwrap().node_count(), 32);
        assert_eq!(read_file("random_11.txt").unwrap().edge_count(), 496);
    }

    fn distance(path: &str, k: u32) -> u32 {
        let g = read_file(path).unwrap();
        let (_, res) = clustering(&g, k);
        res
    }

    #[test]
    fn small_k3() {
        assert_eq!(distance("clustering_small.txt", 3), 3);
    }

    #[test]
    fn small_k2() {
        assert_eq!(distance("clustering_small.txt", 2), 5);
    }

    #[test]
    fn random_14() {
        assert_eq!(distance("random_14.txt", 4), 268);
    }

    #[test]
    fn random_18() {
        assert_eq!(distance("random_18.txt", 4), 512);
    }

    #[test]
    fn random_11() {
        assert_eq!(distance("random_11.txt", 4), 100);
    }

    #[test]
    fn random_1() {
        assert_eq!(distance("random_1.txt", 4), 21);
    }
}

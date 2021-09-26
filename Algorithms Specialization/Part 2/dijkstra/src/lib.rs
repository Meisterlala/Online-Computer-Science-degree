pub mod parser;
use std::collections::HashMap;

use petgraph::graph::EdgeReference;
use petgraph::graph::NodeIndex;
use petgraph::visit::EdgeRef;
use petgraph::Graph;
use petgraph::Undirected;

const TARGET_NODES: [usize; TARGET_COUNT] = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197];
const TARGET_COUNT: usize = 10;

pub fn dijkstra_imported(graph: &Graph<(), u32, Undirected>) -> [u32; TARGET_COUNT] {
    let a = petgraph::algo::dijkstra(graph, NodeIndex::new(0), None, |e| *e.weight());
    hashmap_to_target(&a)
}

fn hashmap_to_target(map: &HashMap<NodeIndex, u32>) -> [u32; TARGET_COUNT] {
    let mut res = [0; TARGET_COUNT];
    for (i, t) in TARGET_NODES.iter().enumerate() {
        res[i] = map[&NodeIndex::new(*t)];
    }
    res
}

pub fn dijkstra(graph: &Graph<(), u32, Undirected>) -> [u32; TARGET_COUNT] {
    let mut x: Vec<NodeIndex> = vec![];
    let mut a: HashMap<NodeIndex, u32> = HashMap::new();

    // Start with 0
    a.insert(NodeIndex::new(0), 0);
    x.push(NodeIndex::new(0));

    for _ in graph.node_indices().skip(1) {
        let mut min = u32::MAX;
        let mut min_edge: Option<EdgeReference<u32>> = None;
        for edge in graph.edge_references() {
            let source = edge.source();
            let target = edge.target();

            if x.contains(&source) && !x.contains(&target) {
                let dist = a.get(&source).unwrap() + edge.weight();

                if dist < min {
                    min = dist;
                    min_edge = Some(edge);
                }
            }
        }

    
        let v_star = min_edge.unwrap().source();
        let w_star = min_edge.unwrap().target();
        
        x.push(w_star);

        let node_dist = a.get(&v_star).expect("Algorithm failed") + min_edge.unwrap().weight();
        a.insert(w_star, node_dist);
    }

    hashmap_to_target(&a)
}

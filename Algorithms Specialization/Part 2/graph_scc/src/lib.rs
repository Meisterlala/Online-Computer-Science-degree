use petgraph::algo::kosaraju_scc;
use petgraph::graph::{IndexType, NodeIndex};

use petgraph::visit::EdgeRef;
use petgraph::{Directed, Graph};
pub mod parser;
use ahash::RandomState;
use std::collections::HashMap;

/// Calculate the length of the 5 biggest scc
/// O(m+n)
pub fn five_scc_imported(graph: &Graph<i32, (), Directed>) -> [u32; 5] {
    let sccs = kosaraju_scc(graph);

    // Find length
    lenghts(sccs)
}

fn lenghts(sccs: Vec<Vec<NodeIndex>>) -> [u32; 5] {
    let mut lengths: Vec<usize> = sccs.iter().map(|scc| scc.len()).collect();
    lengths.sort_by(|a, b| b.cmp(a));
    let res_vec: Vec<u32> = lengths.iter().take(5).map(|i| *i as u32).collect();
    let mut res = [0; 5];
    for i in 0..5 {
        res[i] = res_vec[i];
    }
    res
}

/// Calculate the length of the 5 biggest scc
/// O(m+n)
pub fn five_scc(graph: &Graph<i32, (), Directed>) -> [u32; 5] {
    // reverse
    let res = scc(graph);
    lenghts(res)
}

/// Compute Strongly Connected Components
pub fn scc(graph: &Graph<i32, (), Directed>) -> Vec<Vec<NodeIndex>> {
    let mut t = 0;

    // Fist value is the Node index
    // Second value is the finishing time
    let mut finish_time: HashMap<usize, usize, RandomState> = HashMap::default();

    // Reverse Graph
    let mut reversed = graph.clone();
    reversed.reverse();

    // Recusive Explore
    for node in reversed.node_indices().rev() {
        if !finish_time.contains_key(&node.index()) {
            dfs1(&reversed, node, &mut finish_time, &mut t)
        }
    }
    drop(reversed);

    // Second Pass
    // First value is the Leader index
    // Second value are the Indexes of the nodes in that scc
    let mut sccs: HashMap<usize, Vec<usize>, RandomState> = HashMap::default();
    let mut explored2: HashMap<usize, (), RandomState> = HashMap::default();
    let mut s;

    // Sort nodes by finishing Time
    let mut nodes: Vec<NodeIndex> = graph.node_indices().collect();
    nodes.sort_by(|a, b| {
        finish_time
            .get(&b.index())
            .expect("Unmapped Node")
            .cmp(finish_time.get(&a.index()).expect("Unmapped Node"))
    });

    for node in nodes {
        if !explored2.contains_key(&node.index()) {
            s = node;
            dfs2(graph, node, &mut explored2, &mut sccs, s)
        }
    }

    // Hashmap to Vec<Vec>
    let mut result: Vec<Vec<NodeIndex>> = vec![];
    for nodes in sccs.values() {
        let scc: Vec<NodeIndex> = nodes.iter().map(|n| NodeIndex::from(*n as u32)).collect();
        result.push(scc);
    }
    return result;

    fn dfs1(
        graph: &Graph<i32, (), Directed>,
        i: NodeIndex,
        explored: &mut HashMap<usize, usize, RandomState>,
        t: &mut usize,
    ) {
        // Mark Explored
        debug_assert!(!explored.contains_key(&i.index()));
        explored.insert(i.index(), 0);

        for edge in graph.edges(i) {
            let j = edge.target();
            if !explored.contains_key(&j.index()) {
                dfs1(&graph, j, explored, t);
            }
        }
        *t = *t + 1;
        debug_assert!(explored.contains_key(&i.index()));
        explored.insert(i.index(), *t);
    }

    fn dfs2(
        graph: &Graph<i32, (), Directed>,
        i: NodeIndex,
        explored: &mut HashMap<usize, (), RandomState>,
        scc: &mut HashMap<usize, Vec<usize>, RandomState>,
        s: NodeIndex,
    ) {
        // Mark Explored
        debug_assert!(!explored.contains_key(&i.index()));
        explored.insert(i.index(), ());

        // Set Leader
        if scc.contains_key(&s.index()) {
            let vec = scc.get_mut(&s.index()).unwrap();
            vec.push(i.index());
        } else {
            scc.insert(s.index(), vec![i.index()]);
        }

        for edge in graph.edges(i) {
            let j = edge.target();
            if !explored.contains_key(&j.index()) {
                dfs2(graph, j, explored, scc, s)
            }
        }
        debug_assert!(explored.contains_key(&i.index()));
    }
}

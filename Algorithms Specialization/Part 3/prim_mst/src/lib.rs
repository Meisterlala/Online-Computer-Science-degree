use petgraph::graph::{NodeIndex, UnGraph};
use petgraph::visit::*;

pub fn read_from_file(path: &str) -> Option<UnGraph<(), i32>> {
    // Load File
    let file = std::fs::read_to_string(path).ok()?;
    let mut lines = file.lines();

    // Initilize Graph
    let mut first_line = lines.next()?.split_whitespace();
    let nodes = first_line.next()?.parse::<usize>().ok()?;
    let edges = first_line.next()?.parse::<usize>().ok()?;
    let mut graph = UnGraph::<(), i32>::with_capacity(nodes, edges);

    // Fill Graph
    for line in lines {
        let mut split = line.split_whitespace();
        let n1 = NodeIndex::new(split.next()?.parse::<usize>().ok()? - 1);
        let n2 = NodeIndex::new(split.next()?.parse::<usize>().ok()? - 1);
        let cost = split.next()?.parse::<i32>().ok()?;
        graph.extend_with_edges(&[(n1, n2, cost)]);
    }

    Some(graph)
}

pub fn cost(graph: &UnGraph<(), i32>) -> i128 {
    let mut cost = 0;
    for edge in graph.edge_references() {
        cost += *edge.weight() as i128;
    }
    cost
}

pub fn prim_mst(graph: UnGraph<(), i32>) -> UnGraph<(), i32> {
    // Create new Graph
    let mut mst = UnGraph::<(), i32>::with_capacity(graph.node_count(), graph.edge_count());

    // First node
    let mut mst_nodes = vec![1];

    // For each node
    for _ in 0..graph.node_count() - 1 {
        // Find shortest crossing edges
        let shortest = graph
            .edge_references()
            .filter(|e| {
                // If crossing boundary
                (mst_nodes.contains(&e.source().index())
                    && !mst_nodes.contains(&e.target().index()))
                    || (!mst_nodes.contains(&e.source().index())
                        && mst_nodes.contains(&e.target().index()))
            })
            .min_by_key(|e| e.weight())
            .unwrap();

        // Add Shortest to mst
        if mst_nodes.contains(&shortest.source().index()) {
            mst_nodes.push(shortest.target().index());
        } else {
            mst_nodes.push(shortest.source().index())
        }
        mst.extend_with_edges(&[(
            NodeIndex::new(shortest.source().index()),
            NodeIndex::new(shortest.target().index()),
            *shortest.weight(),
        )]);
    }

    mst
}

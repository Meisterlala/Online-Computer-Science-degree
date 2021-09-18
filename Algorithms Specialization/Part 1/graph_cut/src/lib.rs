use petgraph::{
    graph::{EdgeIndex, UnGraph},
    visit::EdgeRef,
};

pub mod graph_writer;
use graph_writer::save_graph;

const EXPORT_GRAPHS: bool = false;
const EXPORT_GRAPHS_NAME: &str = "contract_";

/// while there are more than 2 verts:
///     pick a remaining edge (u, v) at random
///     merge u and v into a single vert
///     remove self-loops
/// return cut represented by 2 verts
pub fn random_contraction<T1, T2>(g: &mut UnGraph<T1, T2>) -> usize
where
    T2: Default,
    T1: std::fmt::Debug,
    T2: std::fmt::Debug,
{
    let mut length = g.node_count();

    // Debug Output
    if EXPORT_GRAPHS {
        save_graph(&g, &format!("{}{}", EXPORT_GRAPHS_NAME, length));
    }

    while length > 2 {
        // Pick Node at randon
        let node_index = fastrand::usize(..length);
        let u = g.node_indices().nth(node_index).unwrap();
        let v = g.neighbors(u).nth(0).unwrap();

        // Add new edges from all u-connected nodes to v
        let mut neighbors = g.neighbors(u).detach();
        while let Some(neighbor) = neighbors.next_node(g) {
            g.add_edge(neighbor, v, T2::default());
        }

        // Remove u
        g.remove_node(u);

        // Remove Self-loops
        let mut self_loops = g.edges_connecting(v, v);
        let mut to_remove: Vec<EdgeIndex> = vec![];
        while let Some(self_loop) = self_loops.next() {
            to_remove.push(self_loop.id());
        }
        for edge in to_remove {
            // This loop could be removed with better borrowing
            g.remove_edge(edge);
        }

        length = length - 1;

        // Debug Output
        if EXPORT_GRAPHS {
            save_graph(&g, &format!("{}{}", EXPORT_GRAPHS_NAME, length));
        }
    }

    // Debug Output
    if EXPORT_GRAPHS {
        save_graph(&g, &format!("{}{}", EXPORT_GRAPHS_NAME, length));
    }

    g.edge_count() as usize
}

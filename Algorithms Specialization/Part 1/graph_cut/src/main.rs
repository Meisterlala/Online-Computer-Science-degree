use graph_cut::graph_writer::save_graph;
use petgraph::graph::UnGraph;

fn main() {
    let mut g = UnGraph::<(), ()>::new_undirected();

    let n1 = g.add_node(());
    let n2 = g.add_node(());
    let n3 = g.add_node(());

    g.extend_with_edges(&[(n1, n2), (n1, n3)]);

    save_graph(&g, "test");
}

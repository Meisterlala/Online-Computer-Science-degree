use graph_cut::graph_writer::save_graph;
use graph_cut::random_contraction;
use petgraph::{Graph, Undirected};

#[test]
pub fn simple_example() {
    let mut graph = Graph::<(), (), Undirected, usize>::default();

    let n1 = graph.add_node(());
    let n2 = graph.add_node(());
    let n3 = graph.add_node(());
    let n4 = graph.add_node(());

    graph.extend_with_edges(&[(n1, n2), (n2, n3), (n3, n4), (n4, n1), (n2, n4)]);

    save_graph(&graph, "simple_example_in");
    let res = random_contraction(&mut graph, 99);
    save_graph(&graph, "simple_example_out");
    if ![2, 3].contains(&res) {
        panic!()
    }
}

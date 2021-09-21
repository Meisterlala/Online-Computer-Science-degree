use graph_scc::scc;
use petgraph::{Directed, Graph};

#[test]
fn small_graph() {
    let mut g: Graph<i32, (), Directed> = Graph::new();

    g.extend_with_edges(&[
        (1, 7),
        (7, 4),
        (4, 1),
        (7, 0),
        (0, 6),
        (6, 3),
        (3, 0),
        (6, 8),
        (8, 2),
        (2, 5),
        (5, 8),
    ]);
    g.reverse();

    let res = scc(&g);

    for scc in res {
        assert_eq!(scc.len(), 3);
    }
}

use petgraph::{
    graph::EdgeIndex,
    visit::{EdgeRef, IntoNodeIdentifiers},
    Graph, Undirected,
};

pub mod graph_writer;
use graph_writer::save_graph;

pub mod file;

const EXPORT_GRAPHS: bool = false;
const EXPORT_GRAPHS_NAME: &str = "contract_";

/// while there are more than 2 verts:
///     pick a remaining edge (u, v) at random
///     merge u and v into a single vert
///     remove self-loops
/// return cut represented by 2 verts
pub fn random_contraction<T1, T2>(g: &mut Graph<T1, T2, Undirected, usize>, seed: u64) -> usize
where
    T2: Default,
    T1: std::fmt::Debug,
    T2: std::fmt::Debug,
{
    fastrand::seed(seed);

    let mut length = g.node_count();

    // Debug Output
    if EXPORT_GRAPHS {
        save_graph(&g, &format!("{}{}", EXPORT_GRAPHS_NAME, length));
    }

    while length > 2 {
        // Pick Node at randon

        let mut u;
        let mut v;

        loop {
            let edge_index = fastrand::usize(..g.edge_count());
            let e = g.edge_references().nth(edge_index).unwrap();

            u = e.source();
            v = e.target();

            if u != v {
                break;
            } else {
                g.remove_edge(e.id());
            }
        }

        // has neigbors
        if g.neighbors(u).count() == 0 {
            save_graph(g, "panic");
            panic!();
        };

        assert_ne!(u.index(), v.index());

        // Check that v is not u
        // let mut v = g.edges(u).nth(0).unwrap().target();
        // while v.index() == u.index() {
        //     save_graph(&g, "what");
        //     let mut c = g.edges(u);
        //     let x = c.nth(0).unwrap();
        //     let t = x.target();
        //     print!("{:?}", t);
        //     v = g.edges(u).next().unwrap().target();
        // }

        // Add new edges from all u-connected nodes to v
        let neighbors = g.edges(u);
        let mut to_add = vec![];
        for neighbor in neighbors {
            let n1 = neighbor.target();
            if n1 == u {
                to_add.push(neighbor.source())
            } else {
                to_add.push(n1);
            }
        }
        for neighbor_index in to_add {
            g.add_edge(neighbor_index, v, T2::default());
        }

        // Remove u
        g.remove_node(u);

        // Remove Self-loops
        remove_self_loops(g, v);

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

    for node in g.node_identifiers() {
        remove_self_loops(g, node);
    }

    g.edge_count() as usize
}

fn remove_self_loops<T1, T2>(
    g: &mut Graph<T1, T2, Undirected, usize>,
    v: petgraph::graph::NodeIndex<usize>,
) {
    let self_loops = g.edges_connecting(v, v);
    let mut to_remove: Vec<EdgeIndex<usize>> = vec![];
    for self_loop in self_loops {
        to_remove.push(self_loop.id());
    }
    for edge in to_remove {
        // This loop could be removed with better borrowing
        g.remove_edge(edge);
    }
}

pub fn min_cut<T1, T2>(g: &Graph<T1, T2, Undirected, usize>) -> usize
where
    T2: Default,
    T1: std::fmt::Debug,
    T2: std::fmt::Debug,
    T1: Sync,
    T1: Send,
    T2: Send,
    T2: Sync,
    T2: 'static,
    T1: 'static,
    Graph<T1, T2, Undirected, usize>: Clone,
{
    use std::sync::mpsc::channel;
    use threadpool::ThreadPool;

    let workers = 32;
    let pool = ThreadPool::new(workers);

    let (tx, rx) = channel::<(usize, u64)>();

    // Do random contraction and store smallest result
    let iterations = g.node_count();

    let float = f32::log10(iterations as f32).ceil() * iterations as f32 * iterations as f32;

    let iterations = float.max(5f32) as usize;

    let accuracy = (1f32 - 1f32 / iterations as f32) * 100f32;
    println!(
        "Iterations of random_contraction: {} with accuracy of {:10.6}%",
        iterations, &accuracy
    );

    for x in 0..iterations {
        let tx = tx.clone();
        let mut copy = g.clone();
        let seed = fastrand::u64(..);

        pool.execute(move || {
            let res = random_contraction(&mut copy, seed);
            drop(copy);

            if x % 25 == 0 {
                let progress = x as f32 / iterations as f32 * 100f32;
                eprint!("\rProgress: {:6.2?}% ", progress);
            }

            tx.send((res, seed))
                .expect("channel will be there waiting for the pool");
        });

        if pool.queued_count() > workers * 2 {
            pool.join();
        }
    }

    let min = rx
        .iter()
        .take(iterations)
        .min_by(|x, y| x.0.cmp(&y.0))
        .unwrap();

    let mut min_graph = &mut g.clone();
    random_contraction(&mut min_graph, min.1);
    save_graph(&min_graph, "cut_result");
    eprint!("\r                                           \r");
    min.0
}

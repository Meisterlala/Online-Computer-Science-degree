use prim_mst::*;

fn main() {
    println!("Reading file");
    let g = read_from_file("edges.txt").expect("Could not read File");
    println!("Calculating minimum spanning tree  O(m*n)");
    let mst = prim_mst(g);
    let cost = cost(&mst);
    println!("Combined weights of mst: {}", cost);

    // Debug output
    // println!(
    //     "{:?}",
    //     petgraph::dot::Dot::with_config(&mst, &[petgraph::dot::Config::NodeIndexLabel])
    // );
}

#[cfg(test)]
mod test {

    use super::*;
    use petgraph::{algo::min_spanning_tree, data::FromElements, dot::*, graph::Graph, Undirected};

    fn read_full_graph() -> petgraph::graph::UnGraph<(), i32> {
        let file = read_from_file("edges.txt");
        file.unwrap()
    }

    fn read_graph_test1() -> petgraph::graph::UnGraph<(), i32> {
        let file = read_from_file("edges_test_1.txt");
        file.unwrap()
    }

    fn read_graph_test2() -> petgraph::graph::UnGraph<(), i32> {
        let file = read_from_file("edges_test_2.txt");
        file.unwrap()
    }
    fn read_graph_test3() -> petgraph::graph::UnGraph<(), i32> {
        let file = read_from_file("edges_test_3.txt");
        file.unwrap()
    }

    #[test]
    fn parse_file() {
        assert!(read_from_file("edges.txt").is_some());
        assert!(read_from_file("edges_test_1.txt").is_some());
        assert!(read_from_file("edges_test_2.txt").is_some());
    }

    fn compare_to_lib(graph: Graph<(), i32, Undirected>) {
        let correct = Graph::<(), i32, Undirected>::from_elements(min_spanning_tree(&graph));
        let mine = prim_mst(graph);

        assert_eq!(mine.edge_count(), correct.edge_count());
        assert_eq!(mine.node_count(), correct.node_count());

        assert_eq!(cost(&mine), cost(&correct));

        //  print(&mine);
    }

    #[test]
    fn compare_full() {
        compare_to_lib(read_full_graph());
    }

    #[test]
    fn compare_test1() {
        compare_to_lib(read_graph_test1());
    }

    #[test]
    fn compare_test2() {
        compare_to_lib(read_graph_test2());
    }
    #[test]
    fn compare_test3() {
        compare_to_lib(read_graph_test3());
    }

    #[test]
    fn cost_test1() {
        assert_ne!(cost(&read_graph_test1()), 3);
        assert_eq!(cost(&prim_mst(read_graph_test1())), 3);
    }

    #[test]
    fn cost_test2() {
        assert_ne!(cost(&read_graph_test2()), 7);
        assert_eq!(cost(&prim_mst(read_graph_test2())), 7);
    }

    #[test]
    fn cost_test3() {
        assert_ne!(cost(&read_graph_test3()), -246552);
        assert_eq!(cost(&prim_mst(read_graph_test3())), -246552);
    }

    fn print(graph: &Graph<(), i32, Undirected>) {
        println!("{:?}", Dot::with_config(graph, &[Config::NodeIndexLabel]));
    }
}

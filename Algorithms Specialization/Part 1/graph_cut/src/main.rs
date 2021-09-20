use graph_cut::file::GraphFile;
use graph_cut::{graph_writer::*, min_cut};

fn main() {
    let mut big_graph = GraphFile::new("kargerMinCut.txt").unwrap();
    let converted = big_graph.to_graph();
    save_graph(&converted, "big_one");
    println!("Calculation min_cut of {} Node Graph", converted.node_count());   
    let res = min_cut(&converted);
    println!("Result: {}", res);

}

use petgraph::{
    dot::{
        Config::{EdgeNoLabel, NodeNoLabel},
        Dot,
    },
    Graph,
};

use std::io::Write;

/// Save a Graph to a .dot file
pub fn save_graph<T1, T2, T3>(graph: &Graph<T1, T2, T3>, name: &str)
where
    T1: std::fmt::Debug,
    T2: std::fmt::Debug,
    T3: petgraph::EdgeType,
{
    let config = [EdgeNoLabel, NodeNoLabel];

    let graph = Dot::with_config(graph, &config);
    let dot = format!("{:?}", graph);

    // Write Graph
    let prefix = "graphs/".to_owned();
    let suffix = ".dot".to_owned();
    let full_path = prefix + name + &suffix;

    match std::fs::create_dir_all("graphs") {
        Err(_) => {
            println!("Could not create Folder 'graphs'");
            return;
        }
        _ => (),
    }

    let file = std::fs::OpenOptions::new()
        .write(true)
        .create(true)
        .open(&full_path);
    match file {
        Ok(mut f) => write!(f, "{}", &dot).unwrap(),
        Err(_) => println!("Could not write to file: {}", &full_path),
    }
}

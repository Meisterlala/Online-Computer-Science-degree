use petgraph::dot::Config::*;
use petgraph::graph::NodeIndex;
use petgraph::Graph;
use petgraph::{dot::*, Undirected};
use std::fmt::Debug;
use std::fs::File;
use std::io::{Read, Write};

/// Read a file to a directed graph
pub fn parse_graph(path: &str) -> Option<Graph<(), u32, Undirected>> {
    // read file
    let mut file = File::open(path).ok()?;
    let mut content = String::new();
    file.read_to_string(&mut content).ok()?;

    // Construct Graph
    let mut graph: Graph<(), u32, Undirected> = Graph::new_undirected();
    for line in content.lines() {
        // Check for empty line
        if line.len() < 3 {
            continue;
        }

        let split: Vec<&str> = line.split_whitespace().collect();

        // Convert to i32
        let index: u32 = match split[0].parse() {
            Ok(v) => v,
            Err(_) => continue,
        };

        for i in 1..split.len() {
            let split_touple: Vec<&str> = split[i].split(',').collect();

            let connected_to: u32 = match split_touple[0].parse() {
                Ok(v) => v,
                Err(_) => continue,
            };

            let weight: u32 = match split_touple[1].parse() {
                Ok(v) => v,
                Err(_) => continue,
            };

            // Add edge to Graph, and add new nodes if needed
            graph.extend_with_edges(&[(index, connected_to, weight)]);
        }
    }

    // Remove first 0 Node
    graph.remove_node(NodeIndex::new(0));

    Some(graph)
}

/// Save a Graph to a .dot file
pub fn save_graph<T1, T2>(graph: &Graph<T1, T2, Undirected>, name: &str)
where
    T1: Debug,
    T2: Debug,
{
    let config = [NodeNoLabel];

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
        .truncate(true)
        .open(&full_path);
    match file {
        Ok(mut f) => write!(f, "{}", &dot).unwrap(),
        Err(_) => println!("Could not write to file: {}", &full_path),
    }
}

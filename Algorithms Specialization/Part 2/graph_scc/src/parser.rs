use petgraph::dot::Config::*;
use petgraph::dot::*;
use petgraph::{Directed, Graph};
use std::fs::File;
use std::io::{Read, Write};

use flate2::read::GzDecoder;

/// Read the SCC.txt file to a directed graph
pub fn parse_graph(path: &str) -> Option<Graph<i32, (), Directed>> {
    // read file
    let file = File::open(path).ok()?;
    let mut decoded = GzDecoder::new(file);
    let mut content = String::new();
    decoded.read_to_string(&mut content).ok()?;

    // Construct Graph
    let mut graph: Graph<i32, (), Directed> = Graph::new();
    for line in content.lines() {
        // Check for empty line
        if line.len() < 3 {
            continue;
        }

        let split: Vec<&str> = line.split_whitespace().collect();

        // Line has 2 node indexes
        debug_assert_eq!(split.len(), 2);

        // Convert to i32
        let index: u32 = match split[0].parse() {
            Ok(v) => v,
            Err(_) => continue,
        };

        let connected_to: u32 = match split[1].parse() {
            Ok(v) => v,
            Err(_) => continue,
        };

        // Add edge to Graph, and add new nodes if needed
        graph.extend_with_edges(&[(index, connected_to)]);
    }

    Some(graph)
}

/// Save a Graph to a .dot file
pub fn save_graph(graph: &Graph<i32, (), Directed>, name: &str) {
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

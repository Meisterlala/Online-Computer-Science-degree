#![allow(unused)]

use clustering::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Parsing file");
    let graph = match read_file("clustering1.txt") {
        Ok(g) => g,
        Err(e) => {
            return Err(e);
        }
    };
    println!("Clustering");
    let (clusterd, dist) = clustering(&graph, 4);
    println!("minimum distance of clusters: {}", dist);
    println!("Writing to file \"out.dot\"");
    write_graph(&clusterd, "out.dot");
    println!("Done");
    Ok(())
}

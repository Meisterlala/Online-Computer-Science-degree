use std::io::Write;
use std::panic;
use std::process;
use std::sync::mpsc::{self, Receiver, Sender};
use std::time::Instant;

use std::thread;
const STACK_SIZE: usize = 128 * 1024 * 1024;

use dijkstra::parser::save_graph;
use dijkstra::*;

const SAVE_ONLY: bool = false;

pub fn main() {
    // Load Graph
    print!("Parsing Graph ");
    std::io::stdout().flush().unwrap();
    let mut g = parser::parse_graph("dijkstraData.txt").expect("Could not parse graph");
    g.shrink_to_fit();
    println!("finished with {:?} Nodes", g.node_count());

    // Save graph
    if SAVE_ONLY {
        save_graph(&g, "dijkstra");
        return;
    };

    // Channels
    let (tx, rx): (Sender<(String, _)>, Receiver<(String, _)>) = mpsc::channel();

    // Panic handeling
    let orig_hook = panic::take_hook();
    panic::set_hook(Box::new(move |panic_info| {
        // invoke the default handler and exit the process
        orig_hook(panic_info);
        process::exit(1);
    }));

    let g_clone = g.clone();
    let tx1 = tx.clone();
    let child_me = thread::Builder::new()
        .stack_size(STACK_SIZE)
        .name("Self-implemented".to_string())
        .spawn(move || {
            let t = Instant::now();
            let res = dijkstra(&g_clone);
            tx1.send((
                format!(
                    "Calculating dijkstra with self-implemented function took: {:7}{}",
                    t.elapsed().as_micros(),
                    String::from("µs")
                ),
                res,
            ))
            .unwrap();
        })
        .unwrap();

    let tx2 = tx.clone();
    let child_imported = thread::Builder::new()
        .name("Imported".to_string())
        .spawn(move || {
            let t = Instant::now();
            let res = dijkstra_imported(&g);
            tx2.send((
                format!(
                    "Calculating dijkstra with imported function took:         {:7}{}",
                    t.elapsed().as_micros(),
                    String::from("µs")
                ),
                res,
            ))
            .unwrap();
        })
        .unwrap();

    // Join threads, expecting both to not crash
    let res1 = rx.recv().unwrap();
    println!("{}", res1.0);

    child_me.join().unwrap();
    child_imported.join().unwrap();

    let res2 = rx.recv().unwrap();
    println!("{}", res2.0);

    assert_eq!(
        res1.1, res2.1,
        "Output of Imported funtion and self-implemented are different"
    );

    let outp = res1.1.map(|x| x.to_string()).join(",");

    println!("Shortest Paths: {}", outp);
}

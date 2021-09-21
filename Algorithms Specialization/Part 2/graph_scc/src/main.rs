use std::io::Write;
use std::panic;
use std::process;
use std::sync::mpsc::{self, Receiver, Sender};
use std::time::Instant;

use std::thread;
const STACK_SIZE: usize = 128 * 1024 * 1024;

use graph_scc::*;

pub fn main() {
    // Load Graph
    print!("Parsing Graph ");
    std::io::stdout().flush().unwrap();
    let mut g = parser::parse_graph("SCC.txt").expect("Could not parse graph");
    g.shrink_to_fit();
    println!("finished with {:?} Nodes", g.node_count());

    // Channels
    let (tx, rx): (Sender<(String, [u32; 5])>, Receiver<(String, [u32; 5])>) = mpsc::channel();

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
            let res = five_scc(&g_clone);
            tx1.send((
                format!(
                    "Calculating SCCs with self-implemented function took: {:7}ms",
                    t.elapsed().as_millis()
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
            let res = five_scc_imported(&g);
            tx2.send((
                format!(
                    "Calculating SCCs with imported function took:         {:7}ms",
                    t.elapsed().as_millis()
                ),
                res,
            ))
            .unwrap();
        })
        .unwrap();

    // Join threads, expecting both to not crash
    let res1 = rx.recv().unwrap();
    println!("{}", res1.0);
    let res2 = rx.recv().unwrap();
    println!("{}", res2.0);

    child_me.join().unwrap();
    child_imported.join().unwrap();

    assert_eq!(res1.1, res2.1);

    println!("Five SCC lengths: {:?}", res2.1);
}

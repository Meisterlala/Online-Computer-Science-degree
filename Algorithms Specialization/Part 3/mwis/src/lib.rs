pub type PathGraph = Vec<usize>;

pub fn mwis(weights: &PathGraph) -> (usize, Vec<usize>, Vec<usize>) {
    let mut mwis = vec![0; weights.len()];
    mwis[0] = 0;
    mwis[1] = weights[0];

    let mut solution: Vec<usize> = vec![];

    for i in 2..weights.len() {
        let v1 = mwis[i - 1];
        let v2 = mwis[i - 2] + weights[i];

        if v1 > v2 {
            mwis[i] = v1;
            //solution.push(i - 1);
        } else {
            mwis[i] = v2;
            solution.push(i);
        }
    }
    /*
    // Trace back the path
    let mut solution: Vec<usize> = vec![];
    let mut i = mwis.len() - 1;
    while i > 1 {
        if mwis[i - 1] >= mwis[i - 2] + weights[i] {
            i -= 1;
        } else {
            solution.push(i);
            i -= 2;
        }
    }
    if i == 1 && mwis[i] == weights[i] {
        solution.push(i);
    }
    */

    (mwis[mwis.len() - 1], mwis, solution)
}

pub fn asked(solution: &[usize]) -> [bool; 8] {
    let asked_vertex: [usize; 8] = [1, 2, 3, 4, 17, 117, 517, 997];
    let mut result: [bool; 8] = [false; 8];
    for (i, v) in asked_vertex.iter().enumerate() {
        result[i] = solution.contains(v);
    }
    result
}

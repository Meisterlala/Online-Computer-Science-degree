#[derive(Debug, Clone)]
pub struct Jobs {
    jobs: Vec<Job>,
}

#[derive(Debug, Clone, Copy)]
pub struct Job {
    weight: i32,
    length: i32,
}

pub fn load_from_file(path: String) -> Jobs {
    Jobs {
        jobs: std::fs::read_to_string(path)
            .expect("Unable to read file")
            .lines()
            .skip(1)
            .map(|line| {
                let mut parts = line.split_whitespace();
                Job {
                    weight: parts.next().unwrap().parse().unwrap(),
                    length: parts.next().unwrap().parse().unwrap(),
                }
            })
            .collect(),
    }
}

pub fn schedule_jobs_difference(jobs: &Jobs) -> Jobs {
    let mut jobs = jobs.jobs.clone();
    jobs.sort_by(
        |b, a| match (a.weight - a.length).cmp(&(b.weight - b.length)) {
            std::cmp::Ordering::Less => std::cmp::Ordering::Less,
            std::cmp::Ordering::Greater => std::cmp::Ordering::Greater,
            std::cmp::Ordering::Equal => a.weight.cmp(&b.weight),
        },
    );
    Jobs { jobs }
}

pub fn schedule_jobs_ratio(jobs: &Jobs) -> Jobs {
    let mut jobs = jobs.jobs.clone();
    jobs.sort_by(|b, a| (a.weight as f32 / a.length as f32).partial_cmp(&(b.weight as f32 / b.length as f32)).unwrap());
    Jobs { jobs }
}

pub fn completion_time(jobs: &Jobs) -> u64 {
    let mut running_time: u64 = 0;
    let mut total: u64 = 0;
    for j in &jobs.jobs {
        running_time += j.length as u64;
        total += j.weight as u64 * running_time;
    }
    total
}

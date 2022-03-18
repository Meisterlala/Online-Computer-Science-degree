use scheduled_jobs::*;

fn main() {
    println!("Loading jobs from file...");
    let jobs = load_from_file("jobs.txt".to_string());
    println!("Scheduling jobs...");
    let res_1 = completion_time(&schedule_jobs_difference(&jobs));
    let res_2 = completion_time(&schedule_jobs_ratio(&jobs));
    println!("Sum of weighted completion times:");
    println!("Difference: {}", res_1);
    println!("Ratio:      {}", res_2);
}

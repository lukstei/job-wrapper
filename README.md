# job-wrapper.py

This Python script is a super simple wrapper for jobs run via cron or systemd. It collects the status of the job and writes the result as OpenMetric files to a target folder.

## Requirements

- Python 3
- An OpenMetrics compatible collector to pick up the metric files (e.g. Alloy).
- Some application to display the metrics (e.g. Prometheus + Grafana)

## How to Use

Wrap the job to be executed with job-wrapper.py.

`python3 job-wrapper.py <job-name> <command> [<command args>...]`

- **job-name**: The name of the job (will be used for naming the output files and labels for the metrics)
- **command**: The command which should be executed
- **command args**: Further arguments passed to the command


## Metrics

| Metric Name                         | Description                                                  | Format |
|-------------------------------------|--------------------------------------------------------------|--------|
| `job_success`                       | Indicates if the last job run was successful. Returns 1 for success and 0 for failure. | Gauge  |
| `job_execution_seconds`             | The execution time of the last job run, provided in seconds. | Gauge  |
| `job_last_success_timestamp_seconds`| The Unix timestamp of the last successful job run.          | Gauge  |



## Goals

- Provide a simple wrapper for execution of jobs with cron or systemd
- Manage output of metrics
- Do not use any external libraries, to allow easy deployment


For further information also see the corresponding [blog post]().
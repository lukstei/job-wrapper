#!/usr/bin/env python3

from datetime import datetime
import subprocess
import sys
import time
import os

METRICS_DIR = "<put metrics output dir here>"

def run_script(command):
    """Run the script and return the exit code."""
    start_time = time.time()

    try:
        job_metrics_file = os.path.join(METRICS_DIR, f"job.{job_name}.job.prom")
        result = subprocess.run(command, env=dict(os.environ, JOB_METRICS_FILE=job_metrics_file), shell=False)
        exit_code = result.returncode
    except Exception as e:
        exit_code = -1
        print(e, file=sys.stderr)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return exit_code, execution_time


def write_prometheus_metrics(job_name, success, execution_time):
    """Write Prometheus-compatible metrics to a file."""
    success_metric_name = "job_success"
    execution_time_metric_name = "job_execution_seconds"
    last_success_time_metric_name = "job_last_success_timestamp_seconds"

    job_name_label = '{name="' + job_name + '"}'

    path = os.path.join(METRICS_DIR, f"job.{job_name}.prom")
    with open(path, 'w') as f:
        f.write(f"""# HELP {success_metric_name} Indicates whether the last job run was successful (1 for success, 0 for failure)
# TYPE {success_metric_name} gauge
{success_metric_name}{job_name_label} {1 if success else 0}

# HELP {execution_time_metric_name} Execution time of the last job run in seconds
# TYPE {execution_time_metric_name} gauge
{execution_time_metric_name}{job_name_label} {execution_time}
""")
    
    path = os.path.join(METRICS_DIR, f"job.{job_name}.success.prom")
    if success or not os.path.exists(path):
        time = datetime.now().timestamp() if success else 0

        with open(path, 'w') as f:
            f.write(f"""# HELP {last_success_time_metric_name} Unix timestamp of the last successful job run
# TYPE {last_success_time_metric_name} gauge
{last_success_time_metric_name}{job_name_label} {time}
""")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <job-name> <command>")
        exit(1)
    
    [_, job_name, *command] = sys.argv

    exit_code, execution_time = run_script(command)
    success = exit_code == 0
    write_prometheus_metrics(job_name, success, execution_time)

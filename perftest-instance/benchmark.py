import re
import subprocess
import sys
import time

results_folder = "results"


def benchmark_network():
    # Run the speedtest --list command and capture its output
    command_output = subprocess.check_output(['speedtest', '--list', '--secure'], universal_newlines=True)

    pattern = re.compile(r'^(\d+)\)')

    # Split the output into lines
    lines = command_output.splitlines()

    server_ids = []
    # Extract server IDs from each line
    for line in lines:
        print(line)
        # remove spaces from beginning of line
        line = line.strip()

        if pattern.search(line):
            print(line)
            server_id = pattern.search(line).group(1)
            server_ids.append(server_id)

    speedtest_file = open(f"{results_folder}/speedtest.csv", "w")
    command_output = subprocess.check_output(['speedtest', '--secure', '--csv-header'], universal_newlines=True)
    lines = command_output.splitlines()
    for line in lines:
        speedtest_file.write(line + "\n")

    print("Server IDs:")
    for server_id in server_ids:
        print(f"Running speedtest --server {server_id}")
        command_output = subprocess.check_output(['speedtest', '--server', server_id, '--secure', '--csv'], universal_newlines=True)
        lines = command_output.splitlines()
        for line in lines:
            # print(line)
            speedtest_file.write(line)
            # Server ID,  Sponsor,     Server Name,    Timestamp,                     Distance,             Ping,     Download,               Upload,             Share,    IP Address
            # 40981,      PLJ TELECOM, Grodzisk Maz.,  2024-02-04T09:06:10.430439Z,   345.75656799506464,   40.594,   91236583.45204586,      76620728.64388487, ,          188.163.114.161
        speedtest_file.write("\n")
        time.sleep(5)


def benchmark_cpu():
    for threads in [1, 2, 4, 8, 16]:
        sysbench_file = open(f"{results_folder}/sysbench_cpu_{threads}.csv", "w")
        command_output = subprocess.check_output(['sysbench', 'cpu', '--histogram=on', '--cpu-max-prime=20000', '--threads={}'.format(threads), 'run'], universal_newlines=True)
        # sysbench cpu --histogram=on run
        lines = command_output.splitlines()
        for line in lines:
            sysbench_file.write(line + "\n")
        sysbench_file.write("\n")
        time.sleep(5)


def benchmark_memory():
    for threads in [1, 2, 4, 8, 16]:
        sysbench_file = open(f"{results_folder}/sysbench_memory_{threads}.csv", "w")
        command_output = subprocess.check_output(['sysbench', 'memory', '--histogram=on', '--threads={}'.format(threads), 'run'], universal_newlines=True)
        # sysbench cpu --histogram=on run
        lines = command_output.splitlines()
        for line in lines:
            sysbench_file.write(line + "\n")
        sysbench_file.write("\n")
        time.sleep(5)


def get_cpuinfo():
    sysbench_file = open(f"{results_folder}/cpuinfo.raw", "w")
    command_output = subprocess.check_output(['cat', '/proc/cpuinfo'], universal_newlines=True)
    lines = command_output.splitlines()
    for line in lines:
        sysbench_file.write(line + "\n")
    sysbench_file.write("\n")


def benchmark_disk_prepare_files():
    subprocess.check_output(['sysbench', 'fileio', '--file-total-size=8G', 'prepare'], universal_newlines=True)


def benchmark_disk_remove_files():
    subprocess.check_output(['sysbench', 'fileio', '--file-total-size=8G', 'cleanup'], universal_newlines=True)


def benchmark_disk():
    nproc = 2
    for block_size in ['16K', '32K', '64K', '1M', '64M', '128M']:
        sysbench_file = open(f"{results_folder}/sysbench_disk_{block_size}.csv", "w")
        command_output = subprocess.check_output(
            ['sysbench', 'fileio', '--histogram=on', f'--file-block-size={block_size}', '--file-total-size=8G', '--file-test-mode=rndrw', f'--threads={nproc}', 'run'], universal_newlines=True)
        # sysbench cpu --histogram=on run
        lines = command_output.splitlines()
        for line in lines:
            sysbench_file.write(line + "\n")
        sysbench_file.write("\n")

def free_mem():
    sysbench_file = open(f"{results_folder}/free_mem.raw", "w")
    command_output = subprocess.check_output(['free', '-h'], universal_newlines=True)
    lines = command_output.splitlines()
    for line in lines:
        sysbench_file.write(line + "\n")
    sysbench_file.write("\n")

def package(instance_type):
    subprocess.run(["tar", "-czvf", f"{instance_type}.tar.gz", "results"])


def write_to_s3(instance_type):
    bucket = 'benres2024'
    subprocess.run(["aws", "s3", "cp", f"{instance_type}.tar.gz", f"s3://{bucket}"])


if __name__ == '__main__':
    instance_type = "default"
    if len(sys.argv) > 1:
        instance_type = sys.argv[1]

    get_cpuinfo()
    free_mem()
    benchmark_network()
    time.sleep(5)
    benchmark_cpu()
    time.sleep(5)
    benchmark_memory()
    time.sleep(5)
    benchmark_disk_prepare_files()
    time.sleep(5)
    benchmark_disk()
    benchmark_disk_remove_files()
    package(instance_type)
    write_to_s3(instance_type)

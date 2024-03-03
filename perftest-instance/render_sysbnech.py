import re

import numpy as np
from matplotlib import pyplot as plt

categories = []
values = []
benchmarks = {}


def parse_latency(line):
    matches = re.findall(r'(\d+\.\d+|\d+)', line)
    numbers = [float(match) if '.' in match else int(match) for match in matches]
    categories.append(numbers[0])
    values.append(numbers[1])
    return numbers[0], numbers[1]


def parse_memory(line):
    numbers = re.findall(r'\d+\.\d+', line)
    # Convert the matched strings to float
    numbers = [float(num) for num in numbers]
    return numbers[0], numbers[1]


def parse_cpu(line):
    numbers = re.findall(r'\d+\.\d+', line)
    return float(numbers[0])


def parse_disk(line):
    numbers = re.findall(r'\d+\.\d+', line)
    return float(numbers[0])


def parse_graphs(file_name):
    latency = False
    disk = False

    results = {}
    with open(file_name) as f:
        lines = f.readlines()
        categories.clear()
        values.clear()
        for line in lines:
            if (line == '\n') or (line == ' \n'):
                latency = False
                disk = False

            if latency:
                parse_latency(line)

            if disk:
                if 'read' in line:
                    results['disk_read'] = parse_disk(line)
                else:
                    results['disk_write'] = parse_disk(line)

            if 'distribution' in line:
                latency = True

            if 'MiB transferred' in line:
                results['memory'] = parse_memory(line)[1]

            if 'events per second:' in line:
                results['cpu'] = parse_cpu(line)

            if 'Throughput:' in line:
                disk = True

        results['categories'] = categories
        results['values'] = values

        benchmarks[file_name] = results
        draw_latency_graphs(f'latency/{file_name}.png', results['categories'], results['values'])


def draw_latency_graphs(file_name, categories, values):
    fig = plt.figure(figsize=(16, 9))
    # Plot
    plt.bar(categories, values, color='lightblue')

    plt.plot(categories, values, color='red', linestyle='--', marker='o', label='Line')

    # Adding labels
    plt.xlabel('Timing, ms')
    plt.ylabel('Count')
    plt.title('Results Distribution')

    # Show plot
    # plt.show()
    plt.savefig(file_name, bbox_inches='tight', dpi=300)


def draw_horizontal_bars(benchmarks, type, metric):
    instances = []
    performance = []
    for k in benchmarks.keys():
        instances.append(k)

    for v in benchmarks.values():
        performance.append(v[type])

    plt.figure(figsize=(16, 10))
    fig, ax = plt.subplots()
    y_pos = np.arange(len(instances))

    bar = ax.barh(y_pos, performance, label='Download Speed', align='center', alpha=0.7, color=get_colors(len(instances)), height=0.5)
    for rect in bar:
        width = rect.get_width()
        ax.annotate('{}'.format(width),
                    xy=(width, rect.get_y() + rect.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center')

    ax.set_yticks(y_pos, labels=instances)
    ax.invert_yaxis()
    ax.set_xlabel(f'Performance: {metric}')

    plt.savefig(f'{type}.png', bbox_inches='tight', dpi=300)
    plt.show()


def get_colors(size: int):
    colors = ['#FFA500', '#FF0000', '#008000', '#0000FF', '#800080', '#FFFF00', '#00BFFF', '#FF1493', '#FFD700']
    return colors[:size]


if __name__ == '__main__':
    # parse_graphs("remote/results/sysbench_cpu_1.csv")
    # parse_graphs("remote/results/sysbench_cpu_2.csv")
    # parse_graphs("remote/results/sysbench_cpu_4.csv")
    # parse_graphs("remote/results/sysbench_cpu_8.csv")
    # draw_horizontal_bars(benchmarks, 'cpu', 'events per second')


    # benchmarks = {}
    # parse_graphs("remote/results/sysbench_disk_16K.csv")
    # parse_graphs("remote/results/sysbench_disk_32K.csv")
    # parse_graphs("remote/results/sysbench_disk_64K.csv")
    # parse_graphs("remote/results/sysbench_disk_1M.csv")
    # parse_graphs("remote/results/sysbench_disk_64M.csv")
    # parse_graphs("remote/results/sysbench_disk_128M.csv")
    # draw_horizontal_bars(benchmarks, 'disk_read', 'read, MiB/s')
    # draw_horizontal_bars(benchmarks, 'disk_write', 'written, MiB/s')

    benchmarks = {}
    parse_graphs("remote/results/sysbench_memory_1.csv")
    parse_graphs("remote/results/sysbench_memory_2.csv")
    parse_graphs("remote/results/sysbench_memory_4.csv")
    parse_graphs("remote/results/sysbench_memory_8.csv")
    parse_graphs("remote/results/sysbench_memory_16.csv")
    print(benchmarks)
    draw_horizontal_bars(benchmarks, 'memory', 'transferred MiB/sec')


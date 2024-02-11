import re

from matplotlib import pyplot as plt

categories = []
values = []


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
            if line == '\n':
                latency = False
                disk = False

            if latency:
                parse_latency(line)

            if disk:
                if 'read' in line:
                    results['disk_read'] = parse_disk(line)
                else:
                    results['disk_write'] = parse_disk(line)

            if 'value  ------------- distribution ------------- count' in line:
                latency = True

            if 'MiB transferred' in line:
                results['memory'] = parse_memory(line)

            if 'events per second:' in line:
                results['cpu'] = parse_cpu(line)

            if 'Throughput:' in line:
                disk = True

        results['categories'] = categories
        results['values'] = values

        print(results)
        draw_latency_graphs(f'latency/{file_name}.png',results['categories'], results['values'])


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


if __name__ == '__main__':
    parse_graphs("sysbench.disk.output")

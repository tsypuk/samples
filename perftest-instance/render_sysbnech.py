import re

from matplotlib import pyplot as plt

categories = []
values = []

def parse_latency(line):
    matches = re.findall(r'(\d+\.\d+|\d+)', line)

    # Convert the matched strings to float or int
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


def parse_graphs(file_name):
    latency = False
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            if line == '\n':
                latency = False

            if latency:
                parse_latency(line)

            if 'value  ------------- distribution ------------- count' in line:
                latency = True

            if 'MiB transferred' in line:
                parse_memory(line)
            
            if 'events per second:' in line:
                parse_cpu(line)

def draw_graphs(categories, values):

    # Plot
    plt.bar(categories, values, color='lightblue')

    plt.plot(categories, values, color='red', linestyle='--', marker='o', label='Line')

    # Adding labels
    plt.xlabel('Timing, ms')
    plt.ylabel('Count')
    plt.title('Results Distribution')

    # Show plot
    plt.show()

if __name__ == '__main__':
    parse_graphs("sysbench.memory.output")
    draw_graphs(categories, values)
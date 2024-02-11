import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def render(file):
    # Read CSV file into a DataFrame
    df = pd.read_csv(file)

    # Extract necessary columns
    server_names = df['Server Name']
    download_speeds = df['Download']
    upload_speeds = df['Upload']

    # Plot horizontal bar graph
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(server_names, download_speeds, label='Download Speed', color='red', alpha=0.7)
    ax.barh(server_names, upload_speeds, label='Upload Speed', color='blue', alpha=0.7)

    # Customize the plot
    ax.set_xlabel('Speed (bytes/second)')
    ax.set_title('Download and Upload Speeds for Each Server')
    ax.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()


def render2(file):
    # Read CSV file into a DataFrame
    df = pd.read_csv(file)

    # Extract necessary columns
    server_names = df['Server Name']
    download_speeds = df['Download']
    upload_speeds = df['Upload']

    # Plot horizontal bar graphs for download and upload speeds
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), sharex=True)

    ax1.barh(server_names, download_speeds, label='Download Speed', color='blue', alpha=1)
    ax1.set_title('Download Speeds for Each Server')
    ax1.set_xlabel('Download Speed (bytes/second)')
    ax1.legend()

    ax2.barh(server_names, upload_speeds, label='Upload Speed', color='green', alpha=1)
    ax2.set_title('Upload Speeds for Each Server')
    ax2.set_xlabel('Upload Speed (bytes/second)')
    ax2.legend()

    # Customize the layout
    plt.tight_layout()

    # Show the plot
    plt.show()


def many_files(file_names):
    # Initialize a single plot
    fig, ax = plt.subplots(figsize=(16, 10))

    # Iterate through files and plot download speeds
    for file_name in file_names:
        # Read CSV file into DataFrame
        df = pd.read_csv(file_name)

        # Extract necessary columns
        server_names = df['Server Name']
        download_speeds = df['Download'] / 1024 / 1024

        # Plot horizontal bar graphs for download speeds
        ax.barh(server_names, download_speeds, label=file_name.split('_')[0], alpha=1)

    # Customize the plot
    ax.set_xlabel('Download Speed (in Bytes)')
    ax.set_title('Download Speeds for Different Machines')
    ax.legend()

    # Display the values on each bar
    for i, v in enumerate(ax.patches):
        ax.text(v.get_width() + 3, v.get_y() + 0.5 * v.get_height(), str(round(v.get_width(), 2)), color='black')

    # Show the plot
    plt.show()


def grouped(file_names):
    # Initialize a single plot
    fig, ax = plt.subplots(figsize=(15, 8))

    # Set the number of machines
    num_machines = len(file_names)

    # Set the width of the bars
    bar_width = 0.25

    # Set the index for each server
    index = np.arange(len(8))
    # Iterate through files and plot grouped bars for download speeds
    for i, file_name in enumerate(file_names):
        # Read CSV file into DataFrame
        df = pd.read_csv(file_name)

        # Extract necessary columns
        server_names = df['Server Name']
        download_speeds = df['Download']

        # Plot grouped bars for download speeds
        ax.bar(index + i * bar_width, download_speeds, bar_width, label=file_name.split('_')[0], alpha=0.7)

    # Customize the plot
    ax.set_xlabel('Server Names')
    ax.set_ylabel('Download Speed (in Bytes)')
    ax.set_title('Grouped Download Speeds for Different Servers Across Machines')
    ax.set_xticks(index + (num_machines - 1) * bar_width / 2)
    ax.set_xticklabels(server_names, rotation=45, ha='right')
    ax.legend()

    # Display the values on each bar
    for i, v in enumerate(ax.patches):
        ax.text(v.get_x() + v.get_width() / 2, v.get_height() + 3, str(round(v.get_height(), 2)), color='black', ha='center')

    # Show the plot
    plt.show()


def test(file_names, direction):
    # Sample data (replace this with your actual data)

    data = {}
    for file_name in file_names:
        # Read CSV file into DataFrame
        df = pd.read_csv(file_name)

        # Extract necessary columns
        server_names = df['Server Name']
        server_id = df['Server ID']

        download_speeds = df[direction] / 1024 / 1024

        # round 2 digits after coma
        download_speeds = download_speeds.round(2)

        data['Server Name'] = server_names.array
        data[f'{file_name}'] = download_speeds.array

    df = pd.DataFrame(data)

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_height = 0.25
    index = np.arange(len(df['Server Name']))

    for id, file_name in enumerate(file_names):
        # Plot bars for Machine1
        bar1 = ax.barh(index + id * bar_height, df[file_name], bar_height, label=f'Machine:{file_name}', alpha=0.7)

        # Add annotations for each bar
        for rect in bar1:
            width = rect.get_width()
            ax.annotate('{}'.format(width),
                        xy=(width, rect.get_y() + rect.get_height() / 2),
                        xytext=(3, 0),  # 3 points horizontal offset
                        textcoords="offset points",
                        ha='left', va='center')

    # Plot bars for Machine2
    # bar2 = ax.barh(index + bar_height, df['speedtest_2.csv'], bar_height, label='Machine2', alpha=0.7)

    # Customize the plot
    ax.set_ylabel('Server Name')
    ax.set_xlabel(f'{direction} Speed (in Mbit/sec)')
    ax.set_title(f'Grouped {direction} Speeds for Different Servers')
    ax.set_yticks(index + bar_height)
    ax.set_yticklabels(df['Server Name'])
    ax.legend()

    plt.show()


if __name__ == '__main__':
    # render2('speedtest.csv')
    # render2('speedtest_2.csv')
    # grouped(['speedtest.csv', 'speedtest_2.csv'])
    # test(['speedtest.csv', 'speedtest_2.csv'], 'Download')
    test(['speedtest.csv', 'speedtest_2.csv', 'speedtest_3.csv'], 'Upload')

import os
import json
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def load_multiple_jsons(directory):
    combined_data = []

    # Iterate over all JSON files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                combined_data.append(data)
    return combined_data


# Plotting execution time vs. path length
def plot_time_vs_path_length(data):
    times = []
    path_lengths = []
    labels = []

    for key, value in data.items():
        times.append(value["time"])
        path_lengths.append(value["path_len"])
        labels.append(key)

    plt.figure(figsize=(10, 6))
    plt.scatter(path_lengths, times, color='blue', alpha=0.7)
    for i, label in enumerate(labels):
        plt.text(path_lengths[i], times[i], label, fontsize=9)
    plt.title("Execution Time vs Path Length")
    plt.xlabel("Path Length")
    plt.ylabel("Execution Time")
    plt.grid(True)
    plt.show()


# Path visualization using NetworkX
def plot_paths(data, experiment_key):
    if experiment_key not in data:
        print(f"Experiment {experiment_key} not found.")
        return

    path_data = data[experiment_key]["path"]
    G = nx.DiGraph()

    # Add edges to the graph
    for step in path_data:
        G.add_edge(step["point1"], step["point2"])

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)  # Compute layout
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15, edge_color='black')
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    plt.title(f"Path Visualization for Experiment {experiment_key}")
    plt.axis("off")
    plt.show()


# Plotting efficiency (path length vs. optimal length)
def plot_efficiency(data):
    efficiencies = []
    labels = []

    for key, value in data.items():
        eff = value["path_len"] / value["opt_len"]
        efficiencies.append(eff)
        labels.append(key)

    plt.figure(figsize=(10, 6))
    plt.bar(labels, efficiencies, color='green', alpha=0.7)
    plt.axhline(1, color='red', linestyle='--', label="Optimal")
    plt.title("Efficiency of Path (Path Length / Optimal Length)")
    plt.xlabel("Experiment")
    plt.ylabel("Efficiency")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y')
    plt.show()


# Action count vs. execution time
def plot_actions_vs_time(data):
    actions = []
    times = []
    labels = []

    for key, value in data.items():
        actions.append(value["num_action"])
        times.append(value["time"])
        labels.append(key)

    plt.figure(figsize=(10, 6))
    plt.scatter(actions, times, color='purple', alpha=0.7)
    for i, label in enumerate(labels):
        plt.text(actions[i], times[i], label, fontsize=9)
    plt.title("Number of Actions vs Execution Time")
    plt.xlabel("Number of Actions")
    plt.ylabel("Execution Time")
    plt.grid(True)
    plt.show()


# Usage example:
# directory = "path/to/json/folder"
# data = load_multiple_jsons(directory)
# print(data)

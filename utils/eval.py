import json
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import utils.eval_utils as eu
import os

if __name__ == "__main__":
    exp_dir = "tests_runs"
    exp_dir = "experiment_data/KSY_27_11_2024"
    path = os.path.split(os.getcwd())[0]
    path = os.path.join(path, exp_dir)
    experiments = eu.load_multiple_jsons(path)
    print("Number Of Loaded experiments: ", len(experiments))
    experiment_data = []
    for run in experiments:
        experiment_names = run.keys()
        print(experiment_names)

        # TODO: separate optimize results with first try results
        # TODO: Create graphs for metrics

        """
        List of obtained metrics:
        "path":
        "time": 36.30478501319885,
        "path_len": 1464.1862408303084,
        "opt_len": 1150.7001385688782,
        "num_action": 15
        """
    # eu.plot_time_vs_path_length(data)  # Time vs Path Length
    # eval_utils.plot_paths(data, "15_7")  # Replace "15_7" with the experiment key you want to visualize
    # eval_utils.plot_efficiency(data)  # Efficiency (Path Length / Optimal Length)
    # eval_utils.plot_actions_vs_time(data)  # Actions vs Execution Time
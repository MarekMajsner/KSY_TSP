import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import r2_score
import seaborn as sns

def create_cost_matrix(points):
    cost_matrix = [[0 for j in range(len(points))] for i in range(len(points))]
    for i in range(len(points)):
        for j in range(len(points)):
            cost_matrix[i][j] = math.sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)

    return cost_matrix

def calc_length(sequence, cost_matrix):
    length = 0
    # if len(cost_matrix) == len(sequence):
    #     print("ERROR: cost matrix and sequence dimensions not match!")
    #     return None

    print(len(sequence), len(cost_matrix))

    if len(sequence) == len(cost_matrix):
        sequence.append(sequence[0])

    for i in range(len(sequence) - 1):
        length += cost_matrix[sequence[i]][sequence[i+1]]

    return length


def load_cost_matrices(path_to_problems, problem_files):
    cost_matrices = dict()
    for prob in problem_files:
        with open(os.path.join(path_to_problems, prob), 'r') as file:
            problem_data = json.load(file)
            x_points = []
            y_points = []
            points = []
            for point in problem_data["points"]:
                x_points.append(float(point["x"]))
                y_points.append(float(point["y"]))
                points.append((float(point["x"]), float(point["y"])))

            cost_matrix = create_cost_matrix(points)
            cost_matrices[prob.split(".")[0]] = cost_matrix
    
    return cost_matrices

def produce_ai_df():
    path_to_json = '../experiment_data/AI/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    print(json_files)


    path_to_problems = '../experiments/problems/'
    problem_files = [pos_json for pos_json in os.listdir(path_to_problems) if pos_json.endswith('.json')]
    print(problem_files)
    cost_matrices = load_cost_matrices(path_to_problems, problem_files)
    print(calc_length([1, 3, 2, 4, 0, 1], cost_matrices["0_5_100"]))

    path_to_opt_solutions = "../experiments/solutions/"
    opt_solution_files = [pos_json for pos_json in os.listdir(path_to_opt_solutions) if pos_json.endswith('.json')]
    opt_solutions = dict()
    for sol in opt_solution_files:
        with open(os.path.join(path_to_opt_solutions, sol), 'r') as file:
            solution_data = json.load(file)
            # print(solution_data['map_info']['length'])
            opt_solutions[sol.split(".")[0]] = float(solution_data['map_info']['length'])

    df = pd.DataFrame(columns=['participant', 'name', 'rel_len','len','n_points'])

    for tmp in json_files:
        # Load the JSON data
        file = os.path.join(path_to_json, tmp)
        with open(file) as f:
            json_data = json.load(f)

        # Access the prompt
        prompt = json_data["Prompt"]
        print(f"Prompt: {prompt}")
        

        # Access and print all paths

        for key, value in json_data.items():
            if key != "Prompt":
                print(f"{key}: {value['path']}")
                name_ = key.split(".")[0]
                print(name_)
                print(value['path'])
                length = calc_length(value['path'], cost_matrices[name_])
                opt_len = opt_solutions[name_]

                if (length < opt_len-0.00001):
                    print("WARN: Invalid length")
                    continue

                new_row = {'participant': tmp.split(".")[0],
                            'name': key.split(".")[0],
                            'rel_len': length/opt_len,
                            'len': length,
                            'n_points': int(key.split("_")[1])}

                df.loc[len(df)] = new_row

    print(df)
    # df.boxplot(by='name', column =['rel_len'])
    # x = df[df["name"] == 'CLUADE_IMAGE']['name']
    # y = df[df["name"] == 'CLUADE_IMAGE']['rel_len']
    # plt.scatter(x, y, color='red', s=100, alpha=0.7)
    sns.barplot(
        data=df,
        x='name',
        y='rel_len',
        hue='participant',
        palette='tab10'  # Adjust the color palette if needed
    )
    ax = plt.gca()
    ax.set_ylim([0.9, 1.5])
    plt.grid(axis='both', linestyle='--', alpha=0.7)  # Grid lines for better readability
    plt.title('Comparision of AIs', fontsize=16, weight='bold')  # Title
    plt.xlabel('Problem', fontsize=12)  # X-axis label
    plt.ylabel('Relative length', fontsize=12)  # Y-axis label
    # plt.legend(title='Method', fontsize=10)  # Legend with a title
    plt.legend()
    plt.tight_layout()  # Adjust the layout to avoid clipping
    plt.savefig("../figs/AI_comparision.png", dpi=300, bbox_inches='tight')
    plt.show()

    return df

if __name__ == "__main__":
    print(produce_ai_df())
    
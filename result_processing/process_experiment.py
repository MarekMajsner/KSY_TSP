import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import r2_score

# def time_accuracy_tradeoff():




def produce_df():
    path_to_json = '../experiment_data/KSY_second_run'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    print(json_files)
    # json_files = [json_files[0]]

    df = pd.DataFrame(columns=['participant', 'name', 'rel_len','len','time','num_action', 'n_points'])

    participant = 0
    for file in json_files:
        print(file)
        file = os.path.join(path_to_json, file)
        with open(file) as f:
            d = json.load(f)
            print(d.keys())
            for key in d.keys():    # key == name
                if "OPTIMIZE" in key:
                    continue
                new_row = {"participant": participant,
                           "name": key,
                           "rel_len": d[key]["path_len"]/d[key]["opt_len"],
                           "len": d[key]["path_len"],
                           "time": d[key]["time"],
                           "num_action": d[key]["num_action"],
                           "n_points": int(key.split("_")[1])
                           }
                
                df.loc[len(df)] = new_row

        participant = participant + 1

    print(df)


    x_honza = range(1, 11)#df[df['participant'] == 9]["n_points"]

    df.boxplot(by='name', column =['rel_len'])
    plt.grid(axis='both', linestyle='--', alpha=0.7)  # Grid lines for better readability
    plt.title('Boxplots: relative lengths', fontsize=16, weight='bold')  # Title
    plt.xlabel('Problem', fontsize=12)  # X-axis label
    plt.ylabel('Relative length', fontsize=12)  # Y-axis label
    plt.tight_layout()  # Adjust the layout to avoid clipping
    # plt.savefig("../figs/part_rel_len.png", dpi=300, bbox_inches='tight')
    y_honza = df[df['participant'] == 7]["rel_len"]
    plt.scatter(x_honza, y_honza, color='red', s=100, alpha=0.7)
    plt.show()
    # y_jonas = df[df['participant'] == 0]["rel_len"]
    # y_kriplista = df[df['participant'] == 6]["rel_len"]
    # plt.scatter(x_honza, y_jonas, color='blue', s=100, alpha=0.7)
    # plt.scatter(x_honza, y_kriplista, color='green', s=100, alpha=0.7)
    df.boxplot(by='name', column =['time'])
    plt.grid(axis='both', linestyle='--', alpha=0.7)  # Grid lines for better readability
    plt.title('Boxplots: time to solve problem', fontsize=16, weight='bold')  # Title
    plt.xlabel('Problem', fontsize=12)  # X-axis label
    plt.ylabel('Time', fontsize=12)  # Y-axis label
    plt.tight_layout()  # Adjust the layout to avoid clipping
    # plt.savefig("../figs/part_time.png", dpi=300, bbox_inches='tight')
    y_honza = df[df['participant'] == 7]["time"]
    plt.scatter(x_honza, y_honza, color='red', s=100, alpha=0.7)
    plt.show()
    
    # y_jonas = df[df['participant'] == 0]["time"]
    # y_kriplista = df[df['participant'] == 6]["time"]
    # plt.scatter(x_honza, y_jonas, color='blue', s=100, alpha=0.7)
    # plt.scatter(x_honza, y_kriplista, color='green', s=100, alpha=0.7)
    df.boxplot(by='name', column=['num_action'])
    plt.grid(axis='both', linestyle='--', alpha=0.7)  # Grid lines for better readability
    plt.title('Boxplots: number of actions', fontsize=16, weight='bold')  # Title
    plt.xlabel('Problem', fontsize=12)  # X-axis label
    plt.ylabel('Number of actions', fontsize=12)  # Y-axis label
    plt.tight_layout()  # Adjust the layout to avoid clipping
    
    y_honza = df[df['participant'] == 7]["num_action"]
    # y_jonas = df[df['participant'] == 0]["num_action"]
    # y_kriplista = df[df['participant'] == 6]["num_action"]
    plt.scatter(x_honza, y_honza, color='red', s=100, alpha=0.7)
    # plt.scatter(x_honza, y_jonas, color='blue', s=100, alpha=0.7)
    # plt.scatter(x_honza, y_kriplista, color='green', s=100, alpha=0.7)
    # plt.savefig("../figs/part_num_actions.png", dpi=300, bbox_inches='tight')
    plt.show()

    summary_df = df.groupby('participant', as_index=False).agg({
        'len': 'sum',
        'time': 'sum'
    })
    plt.scatter(summary_df['len'], summary_df['time'], color='yellow', s=100, alpha=0.7)
    plt.scatter(summary_df[summary_df['participant']==1]['len'], summary_df[summary_df['participant']==1]['time'], color='blue', s=100, alpha=0.7)
    plt.scatter(summary_df[summary_df['participant']==0]['len'], summary_df[summary_df['participant']==0]['time'], color='pink', s=100, alpha=0.7)
    plt.scatter(summary_df[summary_df['participant']==2]['len'], summary_df[summary_df['participant']==2]['time'], color='green', s=100, alpha=0.7)

    plt.show()
    # print(summary_df)

    # Example Data: Replace these values with your actual data
    

    # Extract x (difficulty) and y (scores)
    # x = df["n_points"].values
    # y = df["time"].values
    x = df.groupby("n_points")["n_points"].median()[1:]
    y = df.groupby("n_points")["time"].median()[1:]
    print(x)
    print(y)
    

    # Linear Model: y = a + bx
    X_linear = sm.add_constant(x)  # Add intercept
    linear_model = sm.OLS(y, X_linear).fit()

    # Quadratic Model: y = a + bx + cx^2
    X_quadratic = sm.add_constant(np.column_stack((x, x**2)))
    quadratic_model = sm.OLS(y, X_quadratic).fit()

    # Print Model Summaries
    print("Linear Model Summary:")
    print(linear_model.summary())
    print("\nQuadratic Model Summary:")
    print(quadratic_model.summary())

    # Calculate R² for both models
    r2_linear = r2_score(y, linear_model.predict(X_linear))
    r2_quadratic = r2_score(y, quadratic_model.predict(X_quadratic))

    print(f"\nR² (Linear Model): {r2_linear:.4f}")
    print(f"R² (Quadratic Model): {r2_quadratic:.4f}")

    # Visualization
    plt.scatter(x, y, color='blue', label='Data')
    plt.plot(sorted(x), linear_model.predict(sm.add_constant(sorted(x))), color='red', label='Linear Fit')
    plt.plot(sorted(x), quadratic_model.predict(sm.add_constant(np.column_stack((sorted(x), np.array(sorted(x))**2)))), color='green', label='Quadratic Fit')
    plt.grid(axis='both', linestyle='--', alpha=0.7)  # Grid lines for better readability
    plt.title('Relation of time and number of vertices', fontsize=16, weight='bold')  # Title
    plt.xlabel('Number of vertices', fontsize=12)  # X-axis label
    plt.ylabel('Time', fontsize=12)  # Y-axis label
    # plt.legend(title='Fit', fontsize=10)  # Legend with a title
    plt.legend()
    plt.tight_layout()  # Adjust the layout to avoid clipping
    # plt.savefig("../figs/part_fitted.png", dpi=300, bbox_inches='tight')
    plt.show()

    return df

if __name__ == "__main__":
    print(produce_df())
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import r2_score

# def time_accuracy_tradeoff():


if __name__ == "__main__":
    path_to_json = '../experiment_data/KSY_second_run'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    print(json_files)
    # json_files = [json_files[0]]

    df = pd.DataFrame(columns=['participant', 'name', 'rel_len','len','time','num_action', 'n_points'])

    participant = 0
    for file in json_files:
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



    df.boxplot(by='name', column =['rel_len'])
    df.boxplot(by='name', column =['time'])
    df.boxplot(by='name', column=['num_action'])
    plt.show()

    summary_df = df.groupby('participant', as_index=False).agg({
        'len': 'sum',
        'time': 'sum'
    })
    plt.scatter(summary_df['len'], summary_df['time'], color='blue', s=100, alpha=0.7)
    plt.show()
    # print(summary_df)

    # Example Data: Replace these values with your actual data
    

    # Extract x (difficulty) and y (scores)
    # x = df["n_points"].values
    # y = df["time"].values
    x = df.groupby("n_points")["n_points"].median()
    y = df.groupby("n_points")["time"].median()
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
    plt.xlabel('Difficulty (x)')
    plt.ylabel('Score (y)')
    plt.title('Linear vs Quadratic Fit')
    plt.legend()
    plt.show()
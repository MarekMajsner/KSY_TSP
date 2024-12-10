import pandas as pd
import os
import json
import matplotlib.pyplot as plt

if __name__ == "__main__":
    path_to_json = '../experiment_data/KSY_27_11_2024'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    print(json_files)

    df = pd.DataFrame(columns=['name', 'rel_len','len','time','num_action'])

    for file in json_files:
        file = os.path.join('../experiment_data/KSY_27_11_2024', file)
        with open(file) as f:
            d = json.load(f)
            print(d.keys())
            for key in d.keys():    # key == name
                new_row = {"name": key,
                           "rel_len": d[key]["path_len"]/d[key]["opt_len"],
                           "len": d[key]["path_len"],
                           "time": d[key]["time"],
                           "num_action": d[key]["num_action"]}
                
                df.loc[len(df)] = new_row

    print(df)



    df.boxplot(by='name', column =['rel_len'])
    df.boxplot(by='name', column =['time'])
    plt.show()

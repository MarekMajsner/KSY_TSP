import pandas as pd
import os
import json
import matplotlib.pyplot as plt

path_to_json = '../result_processing'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print(json_files)

# Load the JSON data
file = os.path.join(path_to_json, json_files[0])
with open(file) as f:
    json_data = json.load(f)

# Access the prompt
prompt = json_data["Prompt"]
print(f"Prompt: {prompt}")

# Access and print all paths
for key, value in json_data.items():
    if key != "Prompt":
        print(f"{key}: {value['path']}")
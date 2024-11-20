import os
from PIL import Image
import math
import json
import matplotlib.pyplot as plt

class TSP_experiment:
    def __init__(self, map_info=None, map_solution=None, image_path_exp=None, image_path_sol=None):
        print(map_info)
        self.locations = None
        self.image_path_exp = image_path_exp
        if self.image_path_exp:
            try:
                self.image = Image.open(self.image_path_exp)
            except Exception as e:
                raise f"Error loading image: {e}"

        if not map_info is None:
            """ 
            LOAD MAP INFO
            """
            self.map_info = map_info["map_info"]
            self.max_x = float(self.map_info["lim_x_max"])
            self.max_y = float(self.map_info["lim_y_max"])
            self.xscale = 322 / float(self.map_info["lim_x_max"])
            self.x_offset = 5
            """ 
            LOAD EXPERIMENT POINTS
            """
            self.locations = map_info["points"]
            print(self.locations)
            self.points_pos_resize()
            print(self.locations)
        if not map_info is None:
            print("TODO")

        self.optimal_distance = 0
        self.image = None

        # self.image_path_exp = image_path_exp
        self.image_path_sol = None

    def points_pos_resize(self):
        for entry in self.locations:
            self.points_pos_string_to_float(entry)
            self.flip_pos_axis(entry)
            self.scale_pos(entry)
            self.border_offset(entry)

    def border_offset(self,entry):
        entry['x'] = entry['x']+self.x_offset
        entry['y'] = entry['y'] +self.x_offset

    def points_pos_string_to_float(self,entry):
        entry['x'] = float(entry['x'])
        entry['y'] = float(entry['y'])

    def flip_pos_axis(self,entry):
        entry['x'] = entry['x']
        entry['y'] = self.max_y - entry['y']


    def scale_pos(self,entry):
        entry['x'] = entry['x']*self.xscale
        entry['y'] = entry['y']*self.xscale

    def calculate_distance(self, other):
        """Calculate distance to another Location instance."""
        if not isinstance(other, TSP_experiment):
            raise ValueError("Argument must be an instance of Location.")
        self.distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return self.distance

    def display_image(self):
        """Display the image if available."""
        if self.image:
            self.image.show()
        else:
            print("No image to display.")

    def __str__(self):
        return f"Location()"


    # def load_experiment(self,path):

def create_test_exp(name = "0", path=None):
    """
    This function loads single experiment specified by number
    (It is expected that all experiment names are numbers)
    :param name: name of experiment to be loaded
    :param path: Path to experiments folder
    """
    # Load experiment problem
    if path is None:
        path = os.path.split(os.getcwd())[0]
    prob_path = os.path.join(path, "experiments", "problems")
    sol_path = os.path.join(path, "experiments", "solutions")

    json_path = os.path.join(prob_path, name + ".json")
    with open(json_path, "r") as file:
        exp_params = json.load(file)


    print(exp_params)

    png_path = os.path.join(prob_path, name + ".png")
    print(png_path)
    image = Image.open(png_path)
    image_path = png_path
    # print(image.size)
    # Load solution to experiment
    print(exp_params['points'])
    example_exp = TSP_experiment(map_info=exp_params, image_path_exp=png_path, image_path_sol=None)
    return example_exp

def count_directories(path):
    return len(next(os.walk(path))[1])

def list_json_files(directory):
    """
    Returns a list of all JSON file names in the given directory.

    :param directory: Path to the directory to search for JSON files.
    :return: List of JSON file names (with extension).
    """
    try:
        # List all files in the directory and filter for .json files
        json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
        return json_files
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' does not exist.")
        return []
    except PermissionError:
        print(f"Error: Permission denied for accessing the directory '{directory}'.")
        return []

def isEmpty(path):
    if os.path.exists(path) and not os.path.isfile(path):

        # Checking if the directory is empty or not
        if not os.listdir(path):
            print("Empty directory")
        else:
            print("Not empty directory")
    else:
        print("The path is either for a file or not valid")


def find_all_experiments(directory):
    """
    Retrieves all PNG and JSON file pairs in the specified directory.

    Args:
        directory (str): The path to the directory to scan.

    Returns:
        list of tuples: List of (png_file, json_file) pairs.
    """
    # Ensure the directory exists
    if not os.path.isdir(directory):
        raise ValueError(f"The provided path '{directory}' is not a valid directory.")

    # List all files in the directory
    files = os.listdir(directory)

    # Filter files by extensions
    png_files = {os.path.splitext(f)[0]: f for f in files if f.lower().endswith('.png')}
    json_files = {os.path.splitext(f)[0]: f for f in files if f.lower().endswith('.json')}

    # Find matching pairs based on the base file name
    pairs = [(png_files[name], json_files[name]) for name in png_files if name in json_files]

    return pairs

def load_experiments(num_experiments=None, single_experiment=None):
    experiments = []

    path = os.getcwd()
    prob_path = os.path.join(path, "experiments", "problems")
    sol_path = os.path.join(path, "experiments", "solutions")

    if not single_experiment is None:
        print("Running single experiment", single_experiment)

    experiments_pairs = find_all_experiments(prob_path)

    print("Number of experiments:", len(experiments_pairs)/2)
    print(experiments_pairs)
    for i in range(len(experiments_pairs)):
        exp_name_json = experiments_pairs[i][1]
        exp_name_png =  experiments_pairs[i][2]
        print(exp_name_png)
        print(exp_name_json)
        exp_path_png = os.path.join(prob_path, exp_name_png)
        exp_path_json = os.path.join(prob_path, exp_name_json)

        if os.path.isfile(exp_path_json):
            with open(exp_path_json, "r") as file:
                exp_params = json.load(file)

        print(exp_params('map_info'))

        experiments.append(TSP_experiment(map_info=exp_params, image_path_exp=exp_path_png))
    return experiments
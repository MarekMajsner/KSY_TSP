import os
from PIL import Image
import math
import json

IMAGE_BORDER = 5 # NUMBER OF PIXELS FOR THE BLACK BORDER

class TSP_experiment:
    def __init__(self, map_info=None, map_solution=None, image_path_exp=None, image_path_sol=None, name = None):
        """

        :param map_info:
        :param map_solution:
        :param image_path_exp:
        :param image_path_sol:
        """
        self.exp_name = name
        self.image_path_exp = image_path_exp
        self.image_path_sol = image_path_sol
        if self.image_path_exp:
            try:
                self.image = Image.open(self.image_path_exp)
            except Exception as e:
                raise f"Error loading image: {e}"

        if self.image_path_sol:
            try:
                self.sol_image = Image.open(self.image_path_exp)
            except Exception as e:
                raise f"Error loading solution image: {e}"

        """IMAGE BORDER SWITCH CASE"""
        image_border = IMAGE_BORDER
        if "big" in self.exp_name:
            image_border = 12

        if not map_info is None:
            """ 
            LOAD MAP INFO
            """
            image_size = self.image.size
            self.map_info = map_info["map_info"]
            self.max_x = float(self.map_info["lim_x_max"])
            self.max_y = float(self.map_info["lim_y_max"])
            self.xscale = (image_size[0]- 2*image_border) / float(self.map_info["lim_x_max"])
            self.yscale = (image_size[1] - 2*image_border)/ float(self.map_info["lim_y_max"])

            self.border_offset = image_border

            """ 
            LOAD EXPERIMENT POINTS
            """
            self.locations = map_info["points"]
            self.points_pos_resize()

            self.named_locations = {entry['name']: (entry['x'], entry['y']) for entry in self.locations}
            self.num_locations = len(self.named_locations)

        if not map_solution is None:
            self.map_solution = map_solution
            self.optimal_distance = float(self.map_solution["map_info"]["length"])*self.xscale
            self.image_path_sol = None

    def points_pos_resize(self):
        for entry in self.locations:
            self.points_pos_string_to_float(entry)
            self.flip_pos_axis(entry)
            self.scale_pos(entry)
            self.add_border_offset(entry)

    def add_border_offset(self,entry):
        entry['x'] = entry['x'] + self.border_offset
        entry['y'] = entry['y'] + self.border_offset

    def points_pos_string_to_float(self,entry):
        entry['x'] = float(entry['x'])
        entry['y'] = float(entry['y'])

    def flip_pos_axis(self,entry):
        entry['x'] = entry['x']
        entry['y'] = self.max_y - entry['y']

    def scale_pos(self,entry):
        if self.xscale != self.yscale:
            print("SCALING ERROR COULD BE PRESENT NON SQUARE IMAGE")
        entry['x'] = entry['x']*self.xscale
        entry['y'] = entry['y']*self.yscale

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
        return f"TSP_Experiment()"


def create_test_exp(name = "0", path=None):
    """
    This function loads single experiment specified by number
    (It is expected that all experiment names are numbers)
    :param name: name of experiment to be loaded
    :param path: Path to experiments folder
    """
    # Load experiment problem
    if path is None:
        path = os.getcwd()
    prob_path = os.path.join(path, "experiments", "problems")
    sol_path = os.path.join(path, "experiments", "solutions")

    json_path = os.path.join(prob_path, name + ".json")
    with open(json_path, "r") as file:
        exp_params = json.load(file)

    json_path_solution = os.path.join(sol_path, name + ".json")

    with open(json_path_solution, "r") as file:
        solution_params = json.load(file)

    png_path = os.path.join(prob_path, name + ".png")
    png_path_solution = os.path.join(prob_path, name + ".png")
    example_exp = TSP_experiment(map_info=exp_params, map_solution=solution_params,
                                 image_path_exp=png_path, image_path_sol=png_path_solution, name=name)
    return example_exp

def list_json_files(directory):
    """
    Returns a list of all JSON file names in the given directory.

    :param directory: Path to the directory to search for JSON files.
    :return: List of JSON file names (with extension).
    """
    try:
        # List all files in the directory and filter for .json files
        json_files = [os.path.splitext(file)[0] for file in os.listdir(directory) if file.endswith('.json')]
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


def load_experiments(args=None):
    if not args.name is None:
        example_exp = create_test_exp(args.name)
        return [example_exp]

    experiments = []

    path = os.getcwd()
    prob_path = os.path.join(path, "experiments", "problems")
    experiment_names = list_json_files(prob_path)

    print("Number of experiments:", len(experiment_names))
    for exp_name in experiment_names:
        experiment = create_test_exp(exp_name,path)
        experiments.append(experiment)
        print("Loaded experiment: ", exp_name)
    return experiments
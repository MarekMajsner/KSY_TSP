import os
from PIL import Image
import math
import json
import matplotlib.pyplot as plt

class TSP_experiment:
    def __init__(self, locations=None, optimal_distance=0,optimal_solution=None , image_path=None, current_working_dir=None):
        self.locations = locations
        self.optimal_distance = optimal_distance
        self.optimal_solution = optimal_solution
        self.image = None
        self.image_path = image_path
        self.cwd = current_working_dir
        if image_path:
            try:
                self.image = Image.open(image_path)
            except Exception as e:
                print(f"Error loading image: {e}")

    def set_position(self, x, y):
        """Set new x and y positions."""
        self.x = x
        self.y = y

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

    def create_test_exp(self):
        """This function expects the existence of Experiment 0 in /experiments"""
        assert self.cwd is not None
        path = os.path.join(self.cwd, "experiments", "0", "0.json")
        with open(path, "r") as file:
            locations = json.load(file)
        self.locations = locations

        path = os.path.join(self.cwd, "experiments", "0", "0.png")

        self.image = Image.open(path)
        self.image_path = path
        print(self.image.size)


def count_directories(path):
    return len(next(os.walk(path))[1])


def load_experiments(num_experiments=None, single_experiment=None):
    experiments = []

    path = os.getcwd()
    path = os.path.join(path, "experiments")
    if num_experiments is None:
        num_experiments = count_directories(path)
    print("Number of experiments:", num_experiments)
    if not single_experiment is None:
        print("Running sinlge experiment", single_experiment)

    for i in range(num_experiments):
        loc_path = os.path.join(path, str(i), str(i) + ".json")

        # TODO: MAKE THIS WORK ANY NAME OF PNG AND JSON
        # filelist = os.listdir('0')
        # for fichier in filelist[:]:  # filelist[:] makes a copy of filelist.
        #     if not (fichier.endswith(".png")):
        #         filelist.remove(fichier)
        #
        with open(loc_path, "r") as file:
            locations = json.load(file)

        img_path = os.path.join(path , str(i), str(i) + ".png")
        experiments.append(TSP_experiment(locations=locations,image_path=img_path))
    # Create Experiments
    # print(experiments[0].image_path)
    return experiments
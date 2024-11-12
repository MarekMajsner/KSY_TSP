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
        return f"Location(name={self.name}, x={self.x}, y={self.y}, distance={self.distance})"

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
        # plt.imshow(self.image)
        # plt.axis('off')  # Hide the axis
        # plt.show()
        print("III")




def load_experiments():
    cwd = os.getcwd()
    # Load the JSON data
    with open(path, "r") as file:
        locations = json.load(file)

    # Display the loaded locations
    for location in locations:
        print(location)

    # Json loading
    print("Loading",exp_path)

    # Create Experiments
    experiments = []
    return experiments